import http from "@/http-common";

class ExaminationsService {
  getAll() {
    return http.get("/examinations/");
  }

  getByConcern(concernId) {
    return http.get("/examinations/", {
      'params': {
          ...({ 'concern': concernId }),
      }
    })
  }

  get(id) {
    return http.get(`/examinations/${id}/`);
  }

  create(data) {
    return http.post("/examinations/", data);
  }

  update(id, data) {
    return http.put(`/examinations/${id}/`, data);
  }

  delete(id) {
    return http.delete(`/examinations/${id}/`);
  }

  deleteAll() {
    return http.delete(`/examinations/`);
  }
}

export default new ExaminationsService();
