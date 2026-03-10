import json
import ssl
import requests
import websocket
import credenciais

# API da Bitstamp
BITSTAMP_API = "https://www.bitstamp.net/api/v2"


def comprar(quantidade):
    """Compra Bitcoin usando API diretamente"""
    url = f"{BITSTAMP_API}/buy/market/btcusd/"
    auth = (credenciais.KEY, credenciais.SECRET)
    data = {"amount": quantidade}
    response = requests.post(url, auth=auth, data=data)
    print(f"Compra: {response.json()}")


def vender(quantidade):
    """Vende Bitcoin usando API diretamente"""
    url = f"{BITSTAMP_API}/sell/market/btcusd/"
    auth = (credenciais.KEY, credenciais.SECRET)
    data = {"amount": quantidade}
    response = requests.post(url, auth=auth, data=data)
    print(f"Venda: {response.json()}")


def ao_abrir(ws):
    print("Conectado ao WebSocket da Bitstamp")
    subscribe_msg = {
        "event": "bts:subscribe",
        "data": {"channel": "live_trades_btcusd"}
    }
    ws.send(json.dumps(subscribe_msg))


def ao_fechar(ws):
    print("Conexão fechada")


def erro(ws, erro):
    print(f"Erro: {erro}")


def ao_receber_mensagem(ws, mensagem):
    try:
        dados = json.loads(mensagem)
        if 'data' in dados and 'price' in dados['data']:
            price = float(dados['data']['price'])
            print(f"Preço BTC/USD: {price}")

            if price > 10000:
                print("Preço alto - VENDENDO")
                vender(0.001)  # Ajuste a quantidade
            elif price < 8100:
                print("Preço baixo - COMPRANDO")
                comprar(0.001)  # Ajuste a quantidade
            else:
                print("Aguardar...")
    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")


if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        "wss://ws.bitstamp.net",
        on_open=ao_abrir,
        on_close=ao_fechar,
        on_message=ao_receber_mensagem,
        on_error=erro
    )
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})