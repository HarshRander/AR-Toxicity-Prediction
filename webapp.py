from flask import Flask, render_template, request
from rdkit import Chem, DataStructs
from rdkit.Chem import Draw, Descriptors, Crippen, Lipinski, rdMolDescriptors, AllChem
import base64
from io import BytesIO
import joblib
import numpy as np

app = Flask(__name__)

model = joblib.load("outputs/final_model_SVM_random.pkl")
vt = joblib.load("outputs/variance_selector.pkl")
corr_idx = joblib.load("outputs/correlation_indices.pkl")
top_idx = joblib.load("outputs/top150_features.pkl")

def mol_to_features(mol):
    fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius=3, nBits=2048)
    arr = np.zeros((2048,), dtype=np.int8)
    DataStructs.ConvertToNumpyArray(fp, arr)
    x = arr.reshape(1, -1)
    x = vt.transform(x)
    x = x[:, corr_idx]
    x = x[:, top_idx]
    return x

# ==========================================================
# HOME PAGE
# ==========================================================
@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        smiles = request.form.get("smiles")

        try:
            mol = Chem.MolFromSmiles(smiles)
            if mol is None:
                raise ValueError("Invalid SMILES")

            # ---------------------------------------------------
            # Draw Molecule
            # ---------------------------------------------------
            img = Draw.MolToImage(mol, size=(400, 400))
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            image = base64.b64encode(buffer.getvalue()).decode()

            # ---------------------------------------------------
            # Molecular Properties
            # ---------------------------------------------------
            mw = round(Descriptors.MolWt(mol), 2)
            logp = round(Crippen.MolLogP(mol), 2)
            tpsa = round(rdMolDescriptors.CalcTPSA(mol), 2)
            hbd = Lipinski.NumHDonors(mol)
            hba = Lipinski.NumHAcceptors(mol)
            rot = Lipinski.NumRotatableBonds(mol)
            rings = Lipinski.RingCount(mol)
            heavy = mol.GetNumHeavyAtoms()
            csp3 = round(rdMolDescriptors.CalcFractionCSP3(mol), 3)
            formula = rdMolDescriptors.CalcMolFormula(mol)

            # ---------------------------------------------------
            # Lipinski Rule
            # ---------------------------------------------------
            lipinski = {
                "MW < 500": mw < 500,
                "LogP < 5": logp < 5,
                "HBA ≤ 10": hba <= 10,
                "HBD ≤ 5": hbd <= 5
            }

            druglike = all(lipinski.values())

            # ---------------------------------------------------
            # REAL MODEL PREDICTION
            # ---------------------------------------------------
            x = mol_to_features(mol)
            pred = model.predict(x)[0]
            probability = round(model.predict_proba(x)[0][1] * 100, 2)

            prediction = (
                "Potentially Toxic"
                if pred == 1
                else "Non Toxic"
            )

            result = {
                "smiles": smiles,
                "prediction": prediction,
                "probability": probability,
                "image": image,
                "mw": mw,
                "logp": logp,
                "tpsa": tpsa,
                "hbd": hbd,
                "hba": hba,
                "rot": rot,
                "rings": rings,
                "heavy": heavy,
                "csp3": csp3,
                "formula": formula,
                "lipinski": lipinski,
                "druglike": druglike
            }

        except Exception as e:
            result = {
                "error": str(e)
            }

    return render_template(
        "index.html",
        result=result
    )

# ==========================================================
# ABOUT PAGE
# ==========================================================
@app.route("/about")
def about():
    return render_template("about.html")

# ==========================================================
# MODEL PAGE
# ==========================================================
@app.route("/model")
def model_page():
    return render_template("model.html")

# ==========================================================
# CONTACT PAGE
# ==========================================================
@app.route("/contact")
def contact():
    return render_template("contact.html")

# ==========================================================
# MAIN
# ==========================================================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
