# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.utils.resource_client import Resource
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack
import json
import time



class AExpressDetail(api_resource.ApiResource):
	"""
	获取订单物流信息
	"""
	app = 'mall'
	resource = 'express_details'

	@param_required(['woid', 'order_id'])
	def get(args):

		order_id = args['order_id']
		woid = args['woid']
		if int(woid) == 3:
			access_token = 'ahQamDeQgZfrWpdR00CsZ6U%2BoRqZ0tVJK0rr27XW1DKudojNeZ2Kz8RpENSpxPDLtg7OhA5WFTLF8E2%2Btg%2BSvg%3D%3D'
			timestamp = str(long(time.time() * 1000))
			data = {
				'timestamp':timestamp, 'woid': woid, 'order_id':order_id,u'access_token':access_token
				}
			resp = Resource.use('apiserver').get({
								'resource': 'mall.express_details',
								'data': data
				})


		errcode= 0

		if resp:
			code = resp["code"]
			if code == 200:
				order_detail = {}
				data = resp["data"]
				
				for express_detail in data['express_details']:
					for i in ['express_id', 'ftime', 'status', 'id', 'created_at']:
						del express_detail[i]
				return 200,{'express':data, 'success':True}

			if code == 500:
				msg = '获取物流信息请求参数错误或缺少参数'
				errcode = 75001
				watchdog.error("get express detail failed!! errcode:{}, msg:{}".format(errcode,unicode_full_stack()),log_type='OPENAPI_ORDER')
				return errcode,{'express': '{}', 'success':False}
		else:
			errcode = 995995
			watchdog.error("get express detail failed!! errcode:{}, msg:{}".format(errcode,unicode_full_stack()),log_type='OPENAPI_ORDER')
			return errcode,{'express': '{}', 'success':False}
		
