import axios_instance from "@/http-common";

class TransactionRequestsService {
  getAll() {
    return axios_instance.get("api/transaction-requests/");
  }

  get(id) {
    return axios_instance.get(`api/transaction-requests/${id}/`);
  }

  create(data) {
    return axios_instance.post("api/transaction-requests/", data);
  }

  update(id, data) {
    return axios_instance.put(`api/transaction-requests/${id}/`, data);
  }

  delete(id) {
    return axios_instance.delete(`api/transaction-requests/${id}/`);
  }

  deleteAll() {
    return axios_instance.delete(`api/transaction-requests`);
  }
}

export default new TransactionRequestsService();
