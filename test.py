# import razorpay
# import hashlib
# import hmac

# # generated_signature = hmac_sha256(
# #     'order_IAKHXtANe8KwkB' + "|" + 'pay_IAKHt6HcTynKiu', '7DQCW16JtDmORBaSxLrwArPh')

# secret = '7DQCW16JtDmORBaSxLrwArPh'

# signature = hmac.new(
#     key=secret,
#     msg='order_IAKHXtANe8KwkB' + "|" + 'pay_IAKHt6HcTynKiu',
#     digestmod=hashlib.sha256
# )

# if (signature == '5ed4bf66615c3468fa0a8eb684571dd14b5e14e146fef613c5ea8e9aed4f5a7e'):
#     print('payment is successful')


import hashlib
import hmac

secret = '7DQCW16JtDmORBaSxLrwArPh'
# assumes you're using requests for data/sig
data = 'order_IAKHXtANe8KwkB' + "|" + 'pay_IAKHt6HcTynKiu'
signature = '5ed4bf66615c3468fa0a8eb684571dd14b5e14e146fef613c5ea8e9aed4f5a7e'
signature_computed = hmac.new(
    key=secret.encode('utf-8'),
    msg=data.encode('utf-8'),
    digestmod=hashlib.sha256
).hexdigest()
print(signature_computed)
print(signature)
if not hmac.compare_digest(signature, signature_computed):
    print("Invalid payload")
