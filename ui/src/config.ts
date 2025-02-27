export function apiKey(): string {
    return process.env.API_KEY;
}

export function username(): string {
    return process.env.APP_USER;
}

export function password(): string {
    return process.env.PASSWORD;
}

export function stage(): string {
    return process.env.STAGE;
}

export function local(): boolean {
    return stage() === 'local';
}

export function baseURL(): string {
    return `${process.env.BASE_URL}/${local() ? '' : stage()}`;
}

export function applicationsURL(): string {
    return baseURL().concat(`${local() ? '' : '/'}applications`);
}

export function membershipURL(): string {
    return baseURL().concat(`${local() ? '' : '/'}membership`);
}
