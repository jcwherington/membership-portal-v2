import axios, { AxiosRequestConfig } from 'axios';
import Member from '@/model/member';
import { membershipURL, apiKey, local } from '@/config';

async function handler(url, method, payload = null) {
    const requestConfig: AxiosRequestConfig = {
        method: method,
        url: url,
        data: payload,
        validateStatus: null,
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

export async function fetchMembers() {
    const method = 'GET';

    return await handler(membershipURL(), method);
}

export async function fetchMember(id: string) {
    const url = membershipURL().concat(`/${id}`);
    const method = 'GET';
    
    return await handler(url, method);
}

export async function createMember(member: Member) {
    const method = 'POST';
    const data = JSON.stringify(member);
    
    return await handler(membershipURL(), method, data);
};

export async function updateMember(member: Member) {
    const url = membershipURL().concat(`/${member.getId()}`);
    const method = 'PUT';
    const data = JSON.stringify(member);
    
    return await handler(url, method, data);
};

export async function deleteMember(id: string) {
    const method = 'DELETE';
    const url = membershipURL().concat(`/${id}`);
    
    return await handler(url, method);
};
