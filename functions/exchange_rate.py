import requests
import config_files.config as config


def gey_rate(code):
    base_code = code
    api_key = config.er_api
    url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_code}'

    # Making our request
    response = requests.get(url)
    ex = response.json()

    base_r = ex['base_code']
    uah_r = ex['conversion_rates']['UAH']
    usd_r = ex['conversion_rates']['USD']
    eur_r = ex['conversion_rates']['EUR']
    rub_r = ex['conversion_rates']['RUB']
    chf_r = ex['conversion_rates']['CHF']
    gbp_r = ex['conversion_rates']['GBP']
    jpy_r = ex['conversion_rates']['JPY']
    aud_r = ex['conversion_rates']['AUD']
    cad_r = ex['conversion_rates']['CAD']
    time_r = ex['time_last_update_utc'][:ex['time_last_update_utc'].find(':')-3]

    result = f'<u>Today {time_r}:</u>\n' \
             f'<b>1 {base_r} = {uah_r} UAH</b>\n' \
             f'<b>1 {base_r} = {usd_r} USD</b>\n' \
             f'<b>1 {base_r} = {eur_r} EUR</b>\n' \
             f'<b>1 {base_r} = {rub_r} RUB</b>\n' \
             f'1 {base_r} = {gbp_r} GBP\n' \
             f'1 {base_r} = {chf_r} CHF\n' \
             f'1 {base_r} = {jpy_r} JPY\n' \
             f'1 {base_r} = {aud_r} AUD\n' \
             f'1 {base_r} = {cad_r} CAD'

    return result
