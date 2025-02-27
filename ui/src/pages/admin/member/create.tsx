import { useForm, SubmitHandler, Controller } from 'react-hook-form';
import styles from '@/styles/Form.module.css';
import { NextRouter, useRouter } from 'next/router';
import { useState } from 'react';
import dayjs from 'dayjs';
import { DateField } from '@mui/x-date-pickers';
import { INDUSTRIES, DATE_FORMAT } from '@/lib/constants';
import Member from '@/model/member';
import { createMember } from '@/lib/api/membership';
import LargeButton from '@/components/buttons/LargeButton';
import SubmitButton from '@/components/buttons/SubmitButton';
import ErrorComponent from '@/components/Error';


export default function Create(): JSX.Element {
    const router: NextRouter = useRouter();
    const [error, setError] = useState<string | null>(null);

    const addButtonHandler: SubmitHandler<undefined> = async (data: Member) => {
        const newMember = new Member(data);
        const membershipResponse = await createMember(newMember);

        if (membershipResponse.status !== 200) {
            setError(membershipResponse.data.message);
            return;
        }

        router.push('/admin.html');
    }

    const {
        register,
        handleSubmit,
        control
    } = useForm();

    return (
        <>
            {error && <ErrorComponent message={error}/>}
            <div className={styles.container}>
                <form onSubmit={handleSubmit(addButtonHandler)} className={styles.form}>
                    <h1>Create</h1>
                    <div className={styles.formRow}>
                        <label htmlFor="firstName">First Name:</label>
                        <input type="text" id="firstName" {...register('firstName', { required: true })} />
                    </div>

                    <div className={styles.formRow}>
                        <label htmlFor="lastName">Last Name:</label>
                        <input type="text" id="lastName" {...register('lastName', { required: true })} />
                    </div>

                    <div className={styles.formRow}>
                        <label htmlFor="organisation">Organisation:</label>
                        <input type="text" id="organisation" {...register('organisation')} />
                    </div>

                    <div className={styles.formRow}>
                        <label htmlFor="position">Position:</label>
                        <input type="text" id="position" {...register('position')} />
                    </div>

                    <div className={styles.formRow}>
                        <label htmlFor="industry">Industry:</label>
                        <select {...register('industry')}>
                            {INDUSTRIES.map((industry, index) => {
                                return <option key={index} value={industry}>{industry}</option>
                            })}
                        </select>
                    </div>

                    <div className={styles.formRow}>
                        <label htmlFor="email">Email:</label>
                        <input type="email" id="email" {...register('email', { required: true })} />
                    </div>

                    <div className={styles.formRow}>
                        <label htmlFor="dob">Date of Birth:</label>
                        <Controller
                            control={control}
                            rules={{ required: true }}
                            name="dob"
                            defaultValue={dayjs(new Date())}
                            render={({ field: { onChange, value } }) => (
                                <DateField
                                    label={DATE_FORMAT}
                                    value={value || dayjs(new Date())}
                                    onChange={onChange}
                                    format={DATE_FORMAT}
                                    fullWidth
                                />
                            )}
                        />
                    </div>

                    <div className={styles.formRow}>
                        <label htmlFor="city">City:</label>
                        <input type="text" id="city" {...register('city')} />
                    </div>

                    <div className={styles.formRow}>
                        <label htmlFor="mobile">Mobile:</label>
                        <input type="text" id="mobile" {...register('mobile', { pattern: /\d+/ })} />
                    </div>

                    <div className={styles.formRow}>
                        <label htmlFor="postCode">Post Code:</label>
                        <input type="text" id="postCode" {...register('postCode', { pattern: /\d+/ })} />
                    </div>

                    <div className={styles.buttonContainer}>
                        <div className={styles.buttonWrapper}>
                            <SubmitButton>
                                Approve
                            </SubmitButton>
                        </div>
                        <div className={styles.buttonWrapper}>
                            <LargeButton type='cancel' handler={() => {router.push({pathname: '/admin.html'})}} >
                                Cancel
                            </LargeButton>
                        </div>
                    </div>
                </form>
            </div>
        </>
    );
};
