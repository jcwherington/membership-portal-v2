import {NextRouter, useRouter} from 'next/router';
import cookieCutter from 'cookie-cutter'
import { useState, useEffect } from 'react';
import { verifyCredentials, generateToken } from '@/lib/auth';
import Login from '@/components/Login';
import ErrorComponent from '@/components/Error';

export default function Home() {
  const router: NextRouter = useRouter();
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    const token = cookieCutter.get('token');

    if (token) {
      router.push('/admin.html');
    }
  }, [router]);

  const handleLogin = (event) => {
    event.preventDefault();
    const username = event.target.username.value;
    const password = event.target.password.value;

    if (verifyCredentials(username, password)) {
      const token = generateToken({
        username: username, 
        password: password
      });
      
      cookieCutter.set('token', token);

      router.push('/admin.html');
    } 
    else {
      setErrorMessage('Login failed! Please check your credentials');
    }
  };

  return (
    <>
      {errorMessage && <ErrorComponent message={errorMessage}/>}
      <Login handler={handleLogin} />
    </>
  )
}
