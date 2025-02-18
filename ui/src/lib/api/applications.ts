import axios, { AxiosRequestConfig } from 'axios';
import { applicationsURL, apiKey, local } from '../../config';

async function handler(url: string, method: string, payload=null) {
    const requestConfig: AxiosRequestConfig = {
        url: url,
        method: method,
        data: payload,
        headers: {
            'x-api-key': apiKey()
        }
    }

    const result = await axios(requestConfig);

    if (local()) {
        const body = JSON.parse(result.data?.body);
        return {
            status: result.status,
            data:   body
        }
    }

    return result;
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
