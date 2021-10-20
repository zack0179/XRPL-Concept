# -*- coding: utf-8 -*-
"""
Purpose - Proof of concept for creating a token in the XRP Ledger

xrp_poc.py
Zackary E. Scalyer
October 11, 2021
Developer, Prepared for Flight, LLC

input
-------
    currently None

output
--------
    print out steps allong the testing workflow


Notes
-------
  - This is supper simple/unrealistic implamentation for now.
  - 10/12/2021 spliting workflow into helper funs
      developing payment type workflow as a collective of funs

usecases:
-------
payment type workflow
    input
        issue_quantity, currency_code = "XRP",
    1) Connect (testnet)
        -Get credentials from the Testnet Faucet
        - Configure issuer
        - Configure hot
    2) Create trust line from hot to cold address
    3) Send token
    4) Check balances
    output

"""

import xrpl
from xrpl.wallet import generate_faucet_wallet


def connect_testnet():
    '''concection for testing'''

    testnet_url = "https://s.altnet.rippletest.net:51234"
    return xrpl.clients.JsonRpcClient(testnet_url)

def connect_wallets(client):
    '''returns hot and cold wallets connected to testnet'''

    # faucet_url = "https://faucet.altnet.rippletest.net/accounts"
    cold_wallet = generate_faucet_wallet(client, debug=True)
    hot_wallet = generate_faucet_wallet(client, debug=True)
    return hot_wallet, cold_wallet


def config_cold(cold_wallet, client):
    '''configure cold address (issuer)'''

    cold_settings_tx = xrpl.models.transactions.AccountSet(
        account=cold_wallet.classic_address,
        transfer_rate=0,
        tick_size=5,
        domain=bytes.hex("example.com".encode("ASCII")),
        set_flag=xrpl.models.transactions.AccountSetFlag.ASF_DEFAULT_RIPPLE,
    )
    cst_prepared = xrpl.transaction.safe_sign_and_autofill_transaction(
        transaction=cold_settings_tx,
        wallet=cold_wallet,
        client=client,
    )
    return xrpl.transaction.send_reliable_submission(cst_prepared, client)


def config_hot(hot_wallet, client):
    '''Configure hot address'''

    hot_settings_tx = xrpl.models.transactions.AccountSet(
        account=hot_wallet.classic_address,
        set_flag=xrpl.models.transactions.AccountSetFlag.ASF_REQUIRE_AUTH,
    )
    hst_prepared = xrpl.transaction.safe_sign_and_autofill_transaction(
        transaction=hot_settings_tx,
        wallet=hot_wallet,
        client=client,
    )
    return xrpl.transaction.send_reliable_submission(hst_prepared, client)


def create_trust(hot_wallet, cold_wallet, client,
                 currency_code = "XRP", limit = "10000000000"):
    '''Create trust line from hot to cold address'''

    trust_set_tx = xrpl.models.transactions.TrustSet(
        account=hot_wallet.classic_address,
        limit_amount=xrpl.models.amounts.issued_currency_amount.IssuedCurrencyAmount(
            currency=currency_code,
            issuer=cold_wallet.classic_address,
            value=limit,
        )
    )
    ts_prepared = xrpl.transaction.safe_sign_and_autofill_transaction(
        transaction=trust_set_tx,
        wallet=hot_wallet,
        client=client,
    )
    return xrpl.transaction.send_reliable_submission(ts_prepared, client)


def send_token(hot_wallet, cold_wallet, client, issue_quantity,
               currency_code = "XRP"):
    '''send token'''

    send_token_tx = xrpl.models.transactions.Payment(
        account=cold_wallet.classic_address,
        destination=hot_wallet.classic_address,
        amount=xrpl.models.amounts.issued_currency_amount.IssuedCurrencyAmount(
            currency=currency_code,
            issuer=cold_wallet.classic_address,
            value=issue_quantity
        )
    )
    pay_prepared = xrpl.transaction.safe_sign_and_autofill_transaction(
        transaction=send_token_tx,
        wallet=cold_wallet,
        client=client,
    )
    # print(f"Sending {issue_quantity} {currency_code} to {hot_wallet.classic_address}...")
    return xrpl.transaction.send_reliable_submission(pay_prepared, client)



def check_bals(hot_wallet, cold_wallet, client, issue_quantity):
    '''check the balence of wallets post transaction'''

    hot_response = client.request(xrpl.models.requests.AccountLines(
        account=hot_wallet.classic_address,
        ledger_index="validated",
    ))
    cold_response = client.request(xrpl.models.requests.GatewayBalances(
        account=cold_wallet.classic_address,
        ledger_index="validated",
        hotwallet=[hot_wallet.classic_address]
    ))
    return hot_response, cold_response


def xrp_poc(issue_quantity, currency_code = "USD"):
    '''wraper'''

    # 1) Connect (testnet)
    client = connect_testnet()
    hot_wallet, cold_wallet = connect_wallets(client)
    config_cold(cold_wallet, client)
    config_hot(hot_wallet, client)
    # 2) Create trust line from hot to cold address
    create_trust(hot_wallet, cold_wallet, client,
                 currency_code = currency_code)
    # 3) Send token
    send_token(hot_wallet, cold_wallet, client,
               issue_quantity = issue_quantity, currency_code = currency_code)
    # 4) Check balances
    hot_response, cold_response = check_bals(hot_wallet, cold_wallet, client,
                                             issue_quantity = issue_quantity)

    return hot_response, cold_response
