import http from "@/http-common";

class TransactionRequestsService {
  getAll() {
    return http.get("transaction-requests/");
  }

  get(id) {
    return http.get(`transaction-requests/${id}/`);
  }

  create(data) {
    return http.post("transaction-requests/", data);
  }

  update(id, data) {
    return http.put(`transaction-requests/${id}/`, data);
  }

  delete(id) {
    return http.delete(`transaction-requests/${id}/`);
  }

  deleteAll() {
    return http.delete(`transaction-requests`);
  }
}

export default new TransactionRequestsService();
