import styles from '@/styles/Login.module.css';
import { Button } from "@mui/material"
import Image from 'next/image'

const Login = (props: {handler: any}): JSX.Element => {

    return (
        <div className={styles.container}>
            <form onSubmit={props.handler} className={styles.form}>
                <div className={styles.logo}>
                    <Image src="<logo_image>" alt="Logo" />
                </div>    
                <div className={styles.formRow}>
                    <label htmlFor="username">Username</label>
                    <input type="text" id="username" />
                </div>

                <div className={styles.formRow}>
                    <label htmlFor="password">Password</label>
                    <input type="password" id="password" />
                </div>

                <div className={styles.buttonContainer}>
                    <Button
                        type="submit"
                        variant="outlined"
                        color="success"
                        disableElevation
                    > 
                        Login
                    </Button>
                </div>
            </form>
        </div>
    )
}

export default Login;
