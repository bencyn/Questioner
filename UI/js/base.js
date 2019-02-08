class Base{
    constructor() {
      this.baseUrl = "http://127.0.0.1:5000/api/v2";
      // this.baseUrl = "https://bencyn-questioner.herokuapp.com/api/v2";
    }
  
    get(endpoint, token=null) {
      return fetch(`${this.baseUrl}${endpoint}`, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
          "content-type": "application/json"
        }
      });
    }
  
    post(endpoint, data, token = null) {
      return fetch(`${this.baseUrl}${endpoint}`, {
        method: "POST",
        mode:"cors",
        body: JSON.stringify(data),
        headers: {
          Authorization: `Bearer ${token}`,
          "content-type": "application/json"
        }
      });
    }
  
    update(endpoint, token, data = null) {
      return fetch(`${this.baseUrl}${endpoint}`, {
        method: "PUT",
        body: JSON.stringify(data),
        headers: {
          Authorization: `Bearer ${token}`,
          "content-type": "application/json"
        }
      });
    }

    patch(endpoint,token = null) {
      return fetch(`${this.baseUrl}${endpoint}`, {
        method: "PATCH",
        headers: {
          Authorization: `Bearer ${token}`,
          "content-type": "application/json"
        }
      });
    }
  
    delete(endpoint, token) {
      return fetch(`${this.baseUrl}${endpoint}`, {
        method: "DELETE",
        mode:"cors",
        headers: {
          Authorization: `Bearer ${token}`,
          "content-type": "application/json"
        }
      });
    }
  }
  const base = new Base();
  export default base;
  