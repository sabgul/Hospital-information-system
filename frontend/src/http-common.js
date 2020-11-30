import axios from "axios";
import {store} from "./store/store";

const axios_instance = axios.create({
    baseURL: "http://localhost:8000/api/",
    headers: {
        "Content-type": "application/json"
    }
});

axios_instance.interceptors.response.use((response) => { return response; }, (error) => {
    // Return any error which is not due to authentication back to the calling service
    if (error.response.status !== 401) {
        return Promise.reject(error);
    }

    // Logout user if token refresh didn't work
    if (error.config.url === '/token/refresh/') {
        return store.dispatch('logoutUser')
    }

    return store.dispatch('refreshToken')
        .then(() => {
            const config = error.config;

            return new Promise((resolve, reject) => {
                axios.request(config).then(response => {
                    resolve(response);
                }).catch((error) => {
                    reject(error);
                })
            });

        })
        .catch((err) => {
            return Promise.reject(err);
        });
});


axios_instance.defaults.headers = {
    // reloaded on every request -> always current access token
    Authorization: {
        toString() {
            return `Bearer ${store.state.access_token}`
        }
    }
}

export default axios_instance;
