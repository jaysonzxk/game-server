import datetime
import time

from dateutil.relativedelta import relativedelta

from apps.admin.member.models import UserVip
from apps.admin.member.serializers import UserVipCardSerializer
from apps.admin.pay.models import PayChannel
from apps.admin.order.models import PurchaseVipOrders
from apps.admin.order.serializers import PurchaseVipOrdersSerializer
from apps.app.utils.json_response import ErrorResponse, DetailResponse


class Pay(object):

    def payVip(self, vipObj, payChannel, user, payUri):
        months = None
        orderNo = str(
            time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + str(time.time()).replace('.', '')[-7:])
        data = {
            # 'user': user.id,
            # 'vipCard': vipObj.id,
            # 'payChannel': payChannel,
            'realAmount': vipObj.originAmount,
            'payUri': '/'.join(payUri.split('/')[-3:]) if payUri else '',
            'orderNumber': orderNo,
            'status': 0
        }
        if vipObj.vipCardType == 0:
            months = 1
        if vipObj.vipCardType == 1:
            months = 3
        if vipObj.vipCardType == 2:
            months = 6
        if vipObj.vipCardType == 3:
            months = 12
        if payChannel and user:
            # 余额支付
            if payChannel.type == 1:
                if user.balance < vipObj.originAmount:
                    return '余额不足'
                else:
                    userVip = UserVip.objects.filter(user_id=user.id).first()
                    if userVip and userVip.isExpired is True:
                        now = datetime.datetime.today()
                        times = relativedelta(months=months)
                        expiration = now + times
                        userVip.update(expiration=expiration)
                    elif userVip is None:
                        now = datetime.datetime.today()
                        times = relativedelta(months=months)
                        expiration = now + times
                        data = {'user': user.id,
                                'vipCard': vipObj.id,
                                'expiration': expiration,
                                'isExpired': 0,
                                'status': 1
                                }
                        serializer = UserVipCardSerializer(data=data)
                        if serializer.is_valid(raise_exception=True):
                            serializer.save()
                        instance = UserVip.objects.filter(id=serializer.data.get('id')).first()
                        instance.user_id = user.id
                        instance.vipCard_id = vipObj.id
                        instance.save()

                    else:
                        # 续费
                        expiration = userVip.expiration
                        times = relativedelta(months=months)
                        expiration = expiration + times
                        userVip.expiration = expiration
                        userVip.save()
                    balance = float(user.balance) - float(vipObj.originAmount)
                    user.balance = balance
                    user.save()
                serializer = PurchaseVipOrdersSerializer(data=data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                instance = PurchaseVipOrders.objects.filter(id=serializer.data.get('id')).first()
                instance.user_id = user.id
                instance.vipCard_id = vipObj.id
                # instance.description = '余额支付'
                instance.payChannel_id = payChannel
                instance.save()
                return '购买成功'
            # usdt支付
            else:
                payChannelObj = PayChannel.objects.filter(id=payChannel.id).filter(isDel=0).filter(status=1).first()
                userVip = UserVip.objects.filter(user_id=user.id).first()
                if payChannelObj:
                    # data = {
                    #     # 'user': user.id,
                    #     # 'vipCard': vipObj.id,
                    #     # 'payChannel': payChannel,
                    #     'realAmount': vipObj.originAmount,
                    #     'payUri': '/'.join(payUri.split('/')[-3:]),
                    #     'orderNumber': orderNo,
                    #     'status': 0
                    # }
                    serializer = PurchaseVipOrdersSerializer(data=data)
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                    instance = PurchaseVipOrders.objects.filter(id=serializer.data.get('id')).first()
                    instance.user_id = user.id
                    instance.vipCard_id = vipObj.id
                    instance.payChannel_id = payChannel
                    # instance.description = '转账支付'
                    instance.save()
                    return '提交成功,请等待审核'
                else:
                    return '支付通道异常,请稍后再试'
        return False

    # 充值余额
    def rechargeBalance(self, rechargeObj, payChannel, user, payUri):
        months = None
        orderNo = str(
            time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + str(time.time()).replace('.', '')[-7:])
        data = {
            # 'user': user.id,
            # 'vipCard': vipObj.id,
            # 'payChannel': payChannel,
            'realAmount': rechargeObj,
            'payUri': '/'.join(payUri.split('/')[-3:]) if payUri else '',
            'orderNumber': orderNo,
            'status': 0
        }

        if payChannel and user:
            # 余额支付
            if payChannel.type == 1:
                if user.balance < rechargeObj.originAmount:
                    return '余额不足'
                else:
                    userVip = UserVip.objects.filter(user_id=user.id).first()
                    if userVip and userVip.isExpired is True:
                        now = datetime.datetime.today()
                        times = relativedelta(months=months)
                        expiration = now + times
                        userVip.update(expiration=expiration)
                    elif userVip is None:
                        now = datetime.datetime.today()
                        times = relativedelta(months=months)
                        expiration = now + times
                        data = {'user': user.id,
                                'vipCard': vipObj.id,
                                'expiration': expiration,
                                'isExpired': 0,
                                'status': 1
                                }
                        serializer = UserVipCardSerializer(data=data)
                        if serializer.is_valid(raise_exception=True):
                            serializer.save()
                        instance = UserVip.objects.filter(id=serializer.data.get('id')).first()
                        instance.user_id = user.id
                        instance.vipCard_id = vipObj.id
                        instance.save()

                    else:
                        # 续费
                        expiration = userVip.expiration
                        times = relativedelta(months=months)
                        expiration = expiration + times
                        userVip.expiration = expiration
                        userVip.save()
                    balance = float(user.balance) - float(vipObj.originAmount)
                    user.balance = balance
                    user.save()
                serializer = PurchaseVipOrdersSerializer(data=data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                instance = PurchaseVipOrders.objects.filter(id=serializer.data.get('id')).first()
                instance.user_id = user.id
                instance.vipCard_id = vipObj.id
                # instance.description = '余额支付'
                instance.payChannel_id = payChannel
                instance.save()
                return '购买成功'
            # usdt支付
            else:
                payChannelObj = PayChannel.objects.filter(id=payChannel.id).filter(isDel=0).filter(status=1).first()
                userVip = UserVip.objects.filter(user_id=user.id).first()
                if payChannelObj:
                    # data = {
                    #     # 'user': user.id,
                    #     # 'vipCard': vipObj.id,
                    #     # 'payChannel': payChannel,
                    #     'realAmount': vipObj.originAmount,
                    #     'payUri': '/'.join(payUri.split('/')[-3:]),
                    #     'orderNumber': orderNo,
                    #     'status': 0
                    # }
                    serializer = PurchaseVipOrdersSerializer(data=data)
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                    instance = PurchaseVipOrders.objects.filter(id=serializer.data.get('id')).first()
                    instance.user_id = user.id
                    instance.vipCard_id = vipObj.id
                    instance.payChannel_id = payChannel
                    # instance.description = '转账支付'
                    instance.save()
                    return '提交成功,请等待审核'
                else:
                    return '支付通道异常,请稍后再试'
        return False
