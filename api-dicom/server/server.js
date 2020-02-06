var express = require('express');
var bodyParser = require('body-parser');
var app = express();
const fabricNetwork = require('./fabricNetwork')
app.set('view engine', 'ejs');
app.use(bodyParser.json());
urlencoder = bodyParser.urlencoded({ extended: true});
const args = process.argv.slice(2);
const org = args[0];


app.post('/api/createDicom', urlencoder, async function (req, res) {

  try {
    const contract = await fabricNetwork.connectNetwork(`connection-${org}.json`, `../../wallet/wallet-${org}`); 
    console.log(req.body);
    let tx = await contract.submitTransaction('createDicom', req.body.dicomId, req.body.typeExam, req.body.owner);
    res.json({
      status: 'OK - Transaction has been submitted',
      txid: tx.toString()
    });
    console.log('OK - Transaction has been submitted');
  } catch (error) {
    console.error(`Failed to evaluate transaction: ${error}`);
    res.status(500).json({
      error: error
    });
  }

});

app.get('/api/readDicom/:dicomId', async function (req, res) {
  try {
    const contract = await fabricNetwork.connectNetwork(`connection-${org}.json`, `../../wallet/wallet-${org}`);
    const result = await contract.evaluateTransaction('readDicom', req.params.dicomId.toString());
    let response = JSON.parse(result.toString());
    res.json({result:response});
    console.log('OK - Query Successful');
  } catch (error) {
    console.error(`Failed to evaluate transaction: ${error}`);
    res.status(500).json({
      error: error
    });
  }
});

app.post('/api/shareDicom', urlencoder, async function (req, res) {

  try {
    const contract = await fabricNetwork.connectNetwork(`connection-${org}.json`, `../../wallet/wallet-${org}`, req.body.user);
    console.log(req.body);  
    let tx = await contract.submitTransaction('shareDicom', req.body.tokenDicom, req.body.to, req.body.toOrganization, Date.now().toString());
    res.json({
      status: 'OK - Transaction has been submitted',
      txid: tx.toString()
    });
    console.log('OK - Transaction has been submitted');
  } catch (error) {
    console.error(`Failed to evaluate transaction: ${error}`);
    res.status(500).json({
      error: error
    });
  }

});

app.get('/api/readAccessLog/:tokenDicom', async function (req, res) {
  try {
    const contract = await fabricNetwork.connectNetwork(`connection-${org}.json`, `../../wallet/wallet-${org}`);
    const result = await contract.evaluateTransaction('readAccessLog', req.params.tokenDicom.toString());
    let response = JSON.parse(result.toString());
    res.json({result:response});
    console.log('OK - Query Successful');
  } catch (error) {
    console.error(`Failed to evaluate transaction: ${error}`);
    res.status(500).json({
      error: error
    });
  }
})





app.listen(3000, ()=>{
  console.log("***********************************");
  console.log("API server listening at localhost:3000");
  console.log("***********************************");
});
