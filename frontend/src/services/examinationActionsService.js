import http from "@/http-common";

class ExaminationActionsService {
  getAll() {
    return http.get("/examination-actions/");
  }

  getAllByWorker(workerId) {
    return http.get("/examination-actions/", {
      'params': {
        action_manager: workerId,
      }
    })
  }

  getFiltered(filter) {
    const is_action_paid_set = filter.is_action_paid === -1 ? false : true;
    const is_action_paid = filter.is_action_paid === 'true' ? 'true' : 'false';
    const action_manager = filter.action_manager;

    return http.get("/examination-actions/", {
      'params': {
        ...(is_action_paid_set ? { 'is_action_paid': is_action_paid } : {}),
        ...(action_manager !== -1 ? { 'action_manager': action_manager } : {}),
      }
    })
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
