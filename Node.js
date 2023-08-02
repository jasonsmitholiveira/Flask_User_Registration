const express = require('express');
const router = express.Router();
const request = require('request');
const { isBefore } = require('date-fns');

const SERVER_URL = 'https://h-apigateway.conectagov.estaleiro.serpro.gov.br';
const TOKEN_REQUEST_URL = SERVER_URL + '/oauth2/jwt-token';
const CLIENT_ID = '8ddc46f2-f6a3-4077-9e04-74b55de934a5';
const CLIENT_SECRET = '06d4aaac-1412-45f6-bd7c-38b2bef0d706';
const CONSULTA_CPF_URL = SERVER_URL + '/api-cpf-light/v2/consulta/cpf';

const EXPIRATION_WINDOW_IN_SECONDS = 300;

let tokenStorage;

  if (!cpf || !dataNascimento) {
    return res.status(400).json({ error: 'CPF and date of birth are required.' });
  }

  try {
    const response = await getPromiseConsultaCpf(tokenStorage.access_token, cpf);
    const cpfData = JSON.parse(response.body);

    const nomeCompleto = cpfData.nomeCompleto; // Certifique-se de que o campo correto é retornado pela API

    res.status(200).json({ nomeCompleto });
  } catch (error) {
    console.error('Erro na consulta à API CPF Light:', error);
    return res.status(500).json({ error: 'Error fetching data from API.' });
  }

  const access_token = tokenStorage.access_token;

  let listaCpf;
  try {
    const response = await getPromiseConsultaCpf(access_token);
    listaCpf = JSON.parse(response.body);
  } catch (error) {
    console.error('Erro na consulta à API CPF Light:', error);
    return res.status(500).send();
  }

  console.log('---------------------------CONSULTA 1-----------------------------');
  console.log(listaCpf);

  let listaCpf2;
  try {
    const response = await getPromiseConsultaCpf(access_token);
    listaCpf2 = JSON.parse(response.body);
  } catch (error) {
    console.error('Erro na consulta à API CPF Light:', error);
    return res.status(500).send();
  }

  console.log('---------------------------CONSULTA 2-----------------------------');
  console.log(listaCpf2);

  res.status(200).json(listaCpf);
});

function extractExp(tokenJwt) {
  if (tokenJwt) {
    const parts = tokenJwt.split('.');
    if (parts.length === 3) {
      const payload = parts[1];
      if (payload) {
        return JSON.parse(Buffer.from(payload, 'base64')).exp;
      }
    }
  }
  return null;
}

function getPromiseToken() {
  const options = {
    method: 'POST',
    url: TOKEN_REQUEST_URL,
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      Authorization: 'Basic ' + Buffer.from(CLIENT_ID + ':' + CLIENT_SECRET).toString('base64'),
    },
    body: 'grant_type=client_credentials',
  };

  return new Promise(function (resolve, reject) {
    request(options, (err, res, body) => {
      if (err) {
        reject(err);
      } else if (res.statusCode && res.statusCode === 200) {
        resolve({ body, status: res.statusCode });
      } else {
        reject({ body, status: res.statusCode });
      }
    });
  });
}

function getPromiseConsultaCpf(access_token) {
  const options = {
    method: 'POST',
    url: CONSULTA_CPF_URL,
    headers: {
      'Content-Type': 'application/json',
      'x-cpf-usuario': '00000000191',
      Authorization: 'Bearer ' + access_token,
    },
    body: '{"listaCpf": ["00000000272","00000000353","00000000434"]}',
  };

  return new Promise(function (resolve, reject) {
    request(options, (err, res, body) => {
      if (err) {
        reject(err);
      } else if (res.statusCode && res.statusCode === 200) {
        resolve({ body, status: res.statusCode });
      } else {
        reject({ body, status: res.statusCode });
      }
    });
  });
}

module.exports = router;