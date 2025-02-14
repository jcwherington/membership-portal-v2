export function apiKey() {
    return process.env.API_KEY;
}

export function username() {
    return process.env.APP_USER;
}

export function password() {
    return process.env.PASSWORD;
}

export function stage() {
    return process.env.STAGE;
}

export function local() {
    return stage() === 'local';
}

export function baseURL() {
    return `${process.env.BASE_URL}/${local() ? '' : stage()}`;
}

export function applicationsURL() {
    return baseURL().concat(`${local() ? '' : '/'}applications`);
}

export function membershipURL() {
    return baseURL().concat(`${local() ? '' : '/'}membership`);
}
