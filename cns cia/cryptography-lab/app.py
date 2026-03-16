from flask import Flask, render_template, request
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
from algorithms import caesar, vigenere, hill, playfair, railfence, rowcolumn
from algorithms import des_demo, aes_demo, rsa, diffie_hellman, elgamal, ecc_demo

app = Flask(__name__)

ALGOS = [
    {"id":"caesar",  "name":"Caesar Cipher",           "icon":"🔤", "type":"Classical"},
    {"id":"vigenere","name":"Vigenere Cipher",          "icon":"📝", "type":"Classical"},
    {"id":"hill",    "name":"Hill Cipher",              "icon":"🔢", "type":"Classical"},
    {"id":"playfair","name":"Playfair Cipher",          "icon":"🎯", "type":"Classical"},
    {"id":"railfence","name":"Rail Fence Cipher",       "icon":"🚂", "type":"Classical"},
    {"id":"rowcolumn","name":"Row-Column Transposition","icon":"📊", "type":"Classical"},
    {"id":"des",     "name":"DES Algorithm",            "icon":"🔒", "type":"Modern"},
    {"id":"aes",     "name":"AES Algorithm",            "icon":"🛡️", "type":"Modern"},
    {"id":"rsa",     "name":"RSA Algorithm",            "icon":"🔑", "type":"Asymmetric"},
    {"id":"dh",      "name":"Diffie-Hellman",           "icon":"🤝", "type":"Asymmetric"},
    {"id":"elgamal", "name":"ElGamal Cryptography",     "icon":"⚡", "type":"Asymmetric"},
    {"id":"ecc",     "name":"Elliptic Curve Cryptography","icon":"📈","type":"Asymmetric"},
]

@app.route("/")
def index():
    return render_template("index.html", algos=ALGOS)

@app.route("/algo/<name>", methods=["GET","POST"])
def algo_page(name):
    result = None
    error  = None
    data   = {}
    op     = "encrypt"

    if request.method == "POST":
        f = request.form
        op = f.get("op", "encrypt")
        try:
            if name == "caesar":
                r = caesar.encrypt(f["text"], f["shift"]) if op=="encrypt" else caesar.decrypt(f["text"], f["shift"])
                result = r["result"]; data = r

            elif name == "vigenere":
                r = vigenere.encrypt(f["text"], f["key"]) if op=="encrypt" else vigenere.decrypt(f["text"], f["key"])
                result = r["result"]; data = r

            elif name == "hill":
                r = hill.encrypt(f["text"], f["key"]) if op=="encrypt" else hill.decrypt(f["text"], f["key"])
                result = r["result"]; data = r

            elif name == "playfair":
                r = playfair.encrypt(f["text"], f["key"]) if op=="encrypt" else playfair.decrypt(f["text"], f["key"])
                result = r["result"]; data = r

            elif name == "railfence":
                r = railfence.encrypt(f["text"], f["rails"]) if op=="encrypt" else railfence.decrypt(f["text"], f["rails"])
                result = r["result"]; data = r

            elif name == "rowcolumn":
                r = rowcolumn.encrypt(f["text"], f["key"]) if op=="encrypt" else rowcolumn.decrypt(f["text"], f["key"])
                result = r["result"]; data = r

            elif name == "des":
                r = des_demo.des_encrypt_demo(f["text"], f["key"]) if op=="encrypt" else des_demo.des_decrypt_demo(f["text"], f["key"])
                result = r.get("result_hex", r.get("result","")); data = r

            elif name == "aes":
                r = aes_demo.aes_encrypt_demo(f["text"], f["key"]) if op=="encrypt" else aes_demo.aes_decrypt_demo(f["text"], f["key"])
                result = r["result"]; data = r

            elif name == "rsa":
                action = f.get("action","generate")
                if action == "generate":
                    r = rsa.generate_keys(f["p"], f["q"]); result = "Keys generated successfully"; data = r
                elif action == "encrypt":
                    r = rsa.encrypt(f["text"], f["e"], f["n"]); result = r["result"]; data = r
                else:
                    r = rsa.decrypt(f["text"], f["d"], f["n"]); result = r["result"]; data = r

            elif name == "dh":
                r = diffie_hellman.simulate(f["p"], f["g"], f["alice"], f["bob"])
                result = "Shared Secret = " + str(r["shared_secret"]); data = r

            elif name == "elgamal":
                action = f.get("action","generate")
                if action == "generate":
                    r = elgamal.generate_keys(f["p"], f["g"], f.get("x") or None)
                    result = "Keys generated successfully"; data = r
                elif action == "encrypt":
                    r = elgamal.encrypt(f["text"], f["p"], f["g"], f["y"])
                    result = json.dumps(r["encrypted_pairs"]); data = r
                else:
                    pairs = json.loads(f["pairs"])
                    r = elgamal.decrypt(pairs, f["p"], f["x"]); result = r["result"]; data = r

            elif name == "ecc":
                r = ecc_demo.simulate_key_exchange(f["a"],f["b"],f["p"],f["gx"],f["gy"],f["alice_k"],f["bob_k"])
                result = "Shared Secret = " + str(r["shared_secret_alice"]); data = r

        except Exception as e:
            error = str(e)

    return render_template("algo.html", algos=ALGOS, page=name, result=result,
                           error=error, data=data, form=request.form, op=op)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
