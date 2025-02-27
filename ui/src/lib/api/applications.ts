import axios, { AxiosRequestConfig, AxiosResponse } from 'axios';
import { applicationsURL, apiKey, local } from '../../config';

async function handler(url: string, method: string, payload=null): Promise<AxiosResponse> {
    const requestConfig: AxiosRequestConfig = {
        url: url,
        method: method,
        data: payload,
        headers: {
            'x-api-key': apiKey()
        }
    }

    const result: AxiosResponse = await axios(requestConfig);

    if (local()) {
        const body = JSON.parse(result.data?.body);
        return {
            status: result.data.statusCode,
            data:   body
        } as AxiosResponse
    }

    return result;
}

export async function fetchApplications(): Promise<AxiosResponse> {
    const method = 'GET';
    const url: string = applicationsURL()
    
    return handler(url, method);
}

export async function deleteApplication(id: string|number, notify=false): Promise<AxiosResponse> {
    const method = 'DELETE';
    const url = applicationsURL().concat(notify ? `/${id}?notify=true` : `/${id}`);
    const payload = JSON.stringify({
        notify: true
    });
    
    return await handler(url, method, payload);
}
