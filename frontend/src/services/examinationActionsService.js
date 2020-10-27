import http from "@/http-common";

class ExaminationActionsService {
  getAll() {
    return http.get("/examination-actions/");
  }

  get(id) {
    return http.get(`/examination-actions/${id}/`);
  }

  create(data) {
    return http.post("/examination-actions/", data);
  }

  update(id, data) {
    return http.put(`/examination-actions/${id}/`, data);
  }

  delete(id) {
    return http.delete(`/examination-actions/${id}/`);
  }

  deleteAll() {
    return http.delete(`/examination-actions`);
  }
}

export default new ExaminationActionsService();
