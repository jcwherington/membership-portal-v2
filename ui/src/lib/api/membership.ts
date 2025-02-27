import axios, { AxiosRequestConfig, AxiosResponse } from 'axios';
import Member from '@/model/member';
import { membershipURL, apiKey, local } from '@/config';

async function handler(url, method, payload = null): Promise<AxiosResponse> {
    const requestConfig: AxiosRequestConfig = {
        method: method,
        url: url,
        data: payload,
        validateStatus: null,
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

export async function fetchMembers(): Promise<AxiosResponse> {
    const method = 'GET';

    return await handler(membershipURL(), method);
}

export async function fetchMember(id: string): Promise<AxiosResponse> {
    const url: string = membershipURL().concat(`/${id}`);
    const method = 'GET';
    
    return await handler(url, method);
}

export async function createMember(member: Member, notify=false): Promise<AxiosResponse> {
    const method = 'POST';
    const data: string = JSON.stringify(member);
    const url: string = notify ? membershipURL().concat('?notify=true') : membershipURL()
    
    return await handler(url, method, data);
}

export async function updateMember(member: Member): Promise<AxiosResponse> {
    const url: string = membershipURL().concat(`/${member.getId()}`);
    const method = 'PUT';
    const data: string = JSON.stringify(member);
    
    return await handler(url, method, data);
}

export async function deleteMember(id: string): Promise<AxiosResponse> {
    const method = 'DELETE';
    const url: string = membershipURL().concat(`/${id}`);
    
    return await handler(url, method);
}
