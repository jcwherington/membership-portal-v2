import axios, { AxiosRequestConfig } from 'axios';
import { applicationsURL, apiKey } from '../../config';

async function handler(url: string, method: string, payload=null) {
    const requestConfig: AxiosRequestConfig = {
        url: url,
        method: method,
        data: payload,
        headers: {
            'x-api-key': apiKey()
        }
    }

    const res = await axios(requestConfig);
    return res;
}

export async function fetchApplications() {
    const method = 'GET';
    const url = applicationsURL()
    
    return handler(url, method);
}

export async function deleteApplication(id: string|number) {
    const method = 'DELETE';
    const url = applicationsURL().concat(`/${id}`);
    const payload = JSON.stringify({
        notify: true
    });
    
    return await handler(url, method, payload);
}
