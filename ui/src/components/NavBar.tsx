import styles from '@/styles/NavBar.module.css';
import Link from 'next/link';
import Image from 'next/image';
import { useRouter, NextRouter } from 'next/router';
import cookieCutter from 'cookie-cutter';
import SmallButton from './buttons/SmallButton';
import Logo from '../../public/logo-placeholder-image.png';

const NavBar = ({ children }): JSX.Element => {
    const router: NextRouter = useRouter();
    const logout: Function = () => {
        cookieCutter.set('token', '', { expires: new Date(0) });
        router.push('/index.html');
    }

    return (
        <div>
            <nav className={styles.navbar}>
                <div className={styles.logo}>
                    <Image src={Logo} alt="Logo" width={60}/>
                </div>
                <ul className={styles.navLinks}>
                    <li><Link href="/admin.html">Members</Link></li>
                    <li><Link href="/admin/applications.html">Applications</Link></li>
                </ul>
                <div className={styles.logout}>
                    <SmallButton type='logout' data={null} handler={logout} />
                </div>
            </nav>
            <main>
                {children}
            </main>
        </div>
    )
}

export default NavBar;
