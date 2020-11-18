import http from "@/http-common";

class DoctorsReportsService {
  getAll() {
    return http.get("/doctor-reports/");
  }

  getByConcern(concernId) {
    return http.get("/doctor-reports/", {
      'params': {
          ...({ 'about_concern': concernId }),
      }
    })
  }

  get(id) {
    return http.get(`/doctor-reports/${id}/`);
  }

  create(data) {
    return http.post("/doctor-reports/", data);
  }

  update(id, data) {
    return http.put(`/doctor-reports/${id}/`, data);
  }

  delete(id) {
    return http.delete(`/doctor-reports/${id}/`);
  }

  deleteAll() {
    return http.delete(`/doctor-reports/`);
  }
}

export default new DoctorsReportsService();
