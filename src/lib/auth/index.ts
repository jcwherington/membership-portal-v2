import jwt from 'jsonwebtoken';
import { username, password, apiKey } from '../../config'

export function generateToken(payload) {
    return jwt.sign(payload, apiKey(), { expiresIn: '1h' });
};
  
export function verifyToken(token) {
    try {
        return jwt.verify(token, apiKey());
    } catch (error) {
        return null;
    }
};

export function verifyCredentials(submittedUsername, submittedPassword) {
    return submittedUsername === username() && submittedPassword === password();
}
