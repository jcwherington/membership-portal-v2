import { useForm, SubmitHandler, Controller } from 'react-hook-form';
import { useEffect } from 'react';
import { DateField } from '@mui/x-date-pickers';
import { INDUSTRIES, DATE_FORMAT } from '@/lib/constants';
import styles from '@/styles/Form.module.css';
import { NextRouter, useRouter } from 'next/router';
import { useState } from 'react'
import Applicant from '@/model/applicant';
import { createMember } from '@/lib/api/membership';
import { deleteApplication } from '@/lib/api/applications'
import LargeButton from '@/components/buttons/LargeButton';
import SubmitButton from '@/components/buttons/SubmitButton';
import Member from '@/model/member';
import ErrorComponent from '@/components/Error';
import { CircularProgress } from '@mui/material';


export default function Review() {
    const router: NextRouter = useRouter()
    const [error, setError] = useState<string | null>(null)
    const [applicant, setApplicant] = useState<Applicant|null>(null);
    const {
        register,
        reset,
        handleSubmit,
        control
    } = useForm();

    useEffect(() => {
        if(router.query.data) {
            setApplicant(new Applicant(JSON.parse(router.query.data as string)));
        }
    }, [router.query.data])
    
    useEffect(() => {
        if (applicant) {
            const defaultValues = {
                firstName: applicant.getFirstName(),
                lastName: applicant.getLastName(),
                organisation: applicant.getOrganisation(),
                position: applicant.getPosition(),
                industry: applicant.getIndustry(),
                email: applicant.getEmail(),
                dob: applicant.getDOB(),
                city: applicant.getCity(),
                mobile: applicant.getMobile(),
                postCode: applicant.getPostCode()
            }
            reset({...defaultValues})
        }
    }, [applicant, reset])

    const deleteButtonHandler: Function = async (id: string) => {
        const applicationResponse = await deleteApplication(id).then(data => data);

        if (applicationResponse.status !== 200) {
            setError(applicationResponse.data.message);
            return;
        } 

        router.push('/admin/applications.html');
    }

    const addButtonHandler: SubmitHandler<undefined> = async (data: Applicant) => {
        const newMember = new Member(data);
        const membershipResponse = await createMember(newMember);

        if (membershipResponse.status !== 200) {
            setError(membershipResponse.data.message);
            return;
        } 

        const applicationResponse = await deleteApplication(applicant.getId())

        if (applicationResponse.status !== 200) {
            setError(applicationResponse.data.message);
            return;
        } 

        router.push('/admin/applications.html');
    }

    if (!applicant) return <CircularProgress />

    return (
        <>
            {error && <ErrorComponent message={error}/>}
            <div className={styles.container}>
                <form onSubmit={handleSubmit(addButtonHandler)} className={styles.form}>
                    <h1>Review</h1>
                    
                    <div className={styles.formRow} style={{ marginBottom: '1rem' }}>
                        <p>Application Id: </p>
                        <span>{applicant.getId()}</span>
                    </div>

                    <div className={styles.formRow} style={{ marginBottom: '3rem'}}>
                        <p>Application Created: </p>
                        <span>{applicant.getCreatedAt()}</span>
                    </div>

                    <div className={styles.formRow}>
                        <label htmlFor="firstName">First Name:</label>
                        <input type="text" id="firstName"
                        {...register('firstName', { required: true })} />
                    </div>

                    <div className={styles.formRow}>
                        <label htmlFor="lastName">Last Name:</label>
                        <input type="text" id="lastName"
                        {...register('lastName', { required: true })} />
                    </div>

                    <div className={styles.formRow}>
                        <label htmlFor="organisation">Organisation:</label>
                        <input type="text" id="organisation"
                        {...register('organisation')} />
                    </div>

                    <div className={styles.formRow}>
                        <label htmlFor="position">Position:</label>
                        <input type="text" id="position"
                        {...register('position')} />
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
                        <input type="email" id="email"
                        {...register('email', { required: true })} />
                    </div>

                    <div className={styles.formRow}>
                        <label htmlFor="dob">Date of Birth:</label>
                        <Controller
                            control={control}
                            rules={{ required: true }}
                            name="dob"
                            render={({ field: { onChange, value } }) => (
                                <DateField
                                    label={DATE_FORMAT}
                                    value={value}
                                    onChange={onChange}
                                    format={DATE_FORMAT}
                                    fullWidth
                                />
                            )}
                        />
                    </div>

                    <div className={styles.formRow}>
                        <label htmlFor="city">City:</label>
                        <input type="text" id="city"
                        {...register('city')} />
                    </div>

                    <div className={styles.formRow}>
                        <label htmlFor="mobile">Mobile:</label>
                        <input type="text" id="mobile"
                        {...register('mobile', { pattern: /\d+/ })} />
                    </div>

                    <div className={styles.formRow}>
                        <label htmlFor="postCode">Post Code:</label>
                        <input type="text" id="postCode"
                        {...register('postCode', { pattern: /\d+/ })} />
                    </div>

                    <div className={styles.buttonContainer}>
                        <div className={styles.buttonWrapper}>
                            <SubmitButton>
                                Approve
                            </SubmitButton>
                        </div>
                        <div className={styles.buttonWrapper}>
                            <LargeButton type='reject' handler={() => deleteButtonHandler(Number(applicant.getId()))}  >
                                Reject
                            </LargeButton>
                        </div>
                        <div className={styles.buttonWrapper}>
                            <LargeButton type='cancel' handler={() => {router.push({pathname: '/admin/applications.html'})}} >
                                Cancel
                            </LargeButton>
                        </div>
                    </div>
                </form>
            </div>
        </>
    );
};
