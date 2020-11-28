import http from "@/http-common";

class DoctorsService {
  getAll() {
    return http.get("doctors");
  }

  get(id) {
    return http.get(`doctors/${id}`);
  }

  create(data) {
    return http.post("doctors/", data);
  }

  update(id, data) {
    return http.put(`doctors/${id}/`, data);
  }

  delete(id) {
    return http.delete(`doctors/${id}/`);
  }

  deleteWithNewResponsible(idToDelete, newResponsibleId) {
    return http.delete(`doctors/${idToDelete}`, {
      'params': {
        ...({'alt': newResponsibleId}),
      }
    })
  }

  deleteAll() {
    return http.delete(`doctors`);
  }
}

export default new DoctorsService();
