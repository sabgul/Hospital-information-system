import http from "@/http-common";

class ExaminationRequestsService {
  getAll() {
    return http.get("/examination-requests/");
  }

  get(id) {
    return http.get(`/examination-requests/${id}/`);
  }

  create(data) {
    return http.post("/examination-requests/", data);
  }

  update(id, data) {
    return http.put(`/examination-requests/${id}/`, data);
  }

  delete(id) {
    return http.delete(`/examination-requests/${id}/`);
  }

  deleteAll() {
    return http.delete(`/examination-requests`);
  }
}

export default new ExaminationRequestsService();
