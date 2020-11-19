import axios_instance from "@/http-common";

class ExaminationActionsService {
  getAll() {
    return axios_instance.get("api/examination-actions/");
  }

  getAllByWorker(workerId) {
    return axios_instance.get("api/examination-actions/", {
      'params': {
        action_manager: workerId,
      }
    })
  }

  getFiltered(filter) {
    const is_action_paid_set = filter.is_action_paid !== -1;
    const is_action_paid = filter.is_action_paid === 'true' ? 'true' : 'false';
    const action_manager = filter.action_manager;

    return axios_instance.get("api/examination-actions/", {
      'params': {
        ...(is_action_paid_set ? { 'is_action_paid': is_action_paid } : {}),
        ...(action_manager !== -1 ? { 'action_manager': action_manager } : {}),
      }
    })
  }
  
  get(id) {
    return axios_instance.get(`api/examination-actions/${id}/`);
  }

  create(data) {
    return axios_instance.post("api/examination-actions/", data);
  }

  update(id, data) {
    return axios_instance.put(`api/examination-actions/${id}/`, data);
  }

  delete(id) {
    return axios_instance.delete(`api/examination-actions/${id}/`);
  }

  deleteAll() {
    return axios_instance.delete(`api/examination-actions`);
  }
}

export default new ExaminationActionsService();
