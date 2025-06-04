from aiocryptopay import AioCryptoPay, Networks

#TOKEN = "28500:AAVcEJH0pqnXbxEZCvOHt0FbjAldBMSuNKc" # TEST_NET
TOKEN = "133500:AATmMmzbhPkncZSoR7dMRNM43yvwNODy6Xw" # MAIN_NET
NETWORK = Networks.MAIN_NET  

crypto = AioCryptoPay(token=TOKEN, network=NETWORK)


async def create_invoice(amount: float, asset="USDT", expires_in=172800):
    async with crypto:
        invoice = await crypto.create_invoice(asset=asset, amount=amount, expires_in=expires_in)
        return invoice.invoice_id, invoice.bot_invoice_url


async def invoice_status(invoice_id):
    async with crypto:
        invoice = await crypto.get_invoices(invoice_ids=invoice_id)
        return invoice.status 


async def delete_invoice(invoice_id):
    async with crypto:
        invoice = await crypto.delete_invoice(invoice_id=invoice_id)
        return invoice.status 


async def check_invoice_amount(invoice_id):
    async with crypto:
        invoice = await crypto.get_invoices(invoice_ids=invoice_id)
        return invoice.amount 

