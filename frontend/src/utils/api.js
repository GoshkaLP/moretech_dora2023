class Api {
  constructor(data) {
    this.baseUrl = data.baseUrl;
    this.headers = data.headers;
  }

  getBranches() {
    return fetch(`${this.baseUrl}/api/routes/branches`)
    .then((res) => {
      return this._getResponseData(res);
    });
  }

  getShortest() {
    return fetch(`${this.baseUrl}/api/routes/shortest?services_ids=1&services_ids=5&services_ids=9&latitude=55.75974142552072&longitude=37.610742623045255`)
    .then((res) => {
      return this._getResponseData(res);
    });
  }


  _getResponseData(res) {
    if (!res.ok) {
      return Promise.reject(res.status);
    }
    return res.json();
  }
}

const api = new Api({
  baseUrl: "https://7a75-176-12-98-131.ngrok-free.app",
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;