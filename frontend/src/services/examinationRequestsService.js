import http from "@/http-common";

class ExaminationRequestsService {
  getAll() {
    return http.get("/examination-requests/");
  }

  getAllByCurrentUser(currentUserId) {
      return http.get("/examination-requests/", {
      'params': {
        ...({ 'assigned_to': currentUserId }),
      }
    })
  }

  getFiltered(filter) {
    const isStateSet = filter.state.length !== 0;

    return http.get("/examination-requests/", {
      'params': {
        ...(isStateSet ? { 'state': filter.state } : {}),
      }
    })
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
