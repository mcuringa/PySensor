const functions = require("firebase-functions");
const admin = require("firebase-admin");
const { Parser } = require("json2csv");
const secretKeys = require("./keys.js");

admin.initializeApp();
const db = admin.firestore();

// Add data to Firestore
exports.logs = functions.https.onRequest(async (req, res) => {
    if (req.method == "POST") {
        return createLog(req, res);
    }
    if (req.method == "GET") {
        return readLog(req, res);
    }
    return res.status(405).send("Method Not Allowed");

});

async function createLog(req, res) {
    const { secret, username, key, value } = req.body;
    if (secretKeys[secret] !== username) {
        return res.status(403).send("Forbidden");
    }
    if (!key || !value) {
        return res.status(400).send("Bad Request: key and value required");
    }

    const timestamp = await admin.firestore.FieldValue.serverTimestamp();
    db.collection("logs").add({ username, key, value, timestamp });
    return res.status(200).send("Data added successfully");
}


// Get data as CSV
async function readLog(req, res)  {
    const secret = req.query.secret;
    const username = req.query.username;
    if (!username) {
        return res.status(400).send("Bad Request: missing username");
    }

    if (secretKeys[secret] !== username) {
        return res.status(403).send("Forbidden");
    }

    const start = req.query.start;
    const end = req.query.end;
    let query = db.collection("logs").where("username", "==", username);
    if (start) query = query.where("timestamp", ">", start);
    if (end) query = query.where("timestamp", "<", end);

    const snapshot = await query.get();
    const logs = snapshot.docs.map(doc => {
        const data = doc.data();
        data.timestamp = data.timestamp.toDate().toISOString();
        return data;
    });
    const fields = ["key", "value", "timestamp"];
    const json2csvParser = new Parser({ fields });
    const csv = json2csvParser.parse(logs);
    res.setHeader("Content-Disposition", "attachment; filename=logs.csv");
    res.set("Content-Type", "text/csv");
    return res.status(200).send(csv);
};
