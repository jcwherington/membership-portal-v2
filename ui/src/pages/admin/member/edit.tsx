import { useForm, SubmitHandler, Controller } from 'react-hook-form';
import styles from '@/styles/Form.module.css';
import { NextRouter, useRouter } from 'next/router';
import { useState, useEffect } from 'react'
import Member from '@/model/member';
import { INDUSTRIES, DATE_FORMAT } from '@/lib/constants';
import { updateMember } from '@/lib/api/membership';
import CircularProgress from '@mui/material/CircularProgress';
import dayjs from 'dayjs';
import { DateField } from '@mui/x-date-pickers';
import ErrorComponent from '@/components/Error';
import LargeButton from '@/components/buttons/LargeButton';
import SubmitButton from '@/components/buttons/SubmitButton';


export default function Edit() {
    const router: NextRouter = useRouter()
    const [errorMessage, setError] = useState<string | null>(null)
    const [member, setMember] = useState<Member|null>(null);
    const {
        register,
        handleSubmit,
        reset,
        control
    } = useForm();

    useEffect(() => {
        if (member) {
            const defaultValues = {
                firstName: member.getFirstName(),
                lastName: member.getLastName(),
                organisation: member.getOrganisation(),
                position: member.getPosition(),
                industry: member.getIndustry(),
                email: member.getEmail(),
                dob: dayjs(member.getDOB(), { format: DATE_FORMAT }),
                city: member.getCity(),
                mobile: member.getMobile(),
                postCode: member.getPostCode(),
            }
            reset({...defaultValues})
        }
    }, [member, reset])

    useEffect(() => {
        if(router.query.data) {
            setMember(new Member(JSON.parse(router.query.data as string)));
        }
    }, [router.query.data])

    const addButtonHandler: SubmitHandler<undefined> = async (data: any) => {
        const updatedMember = new Member({id: member.getId(), ...data});
        const membershipResponse = await updateMember(updatedMember);

        if (membershipResponse.status !== 200) {
            setError(membershipResponse.data.message);
            return;
        }

        router.push('/admin.html');
    }

    if (!member) return <CircularProgress />

    return (
        <>
            {errorMessage && <ErrorComponent message={errorMessage}/>}
            <div className={styles.container}>
                <form onSubmit={handleSubmit(addButtonHandler)} className={styles.form}>
                    <h1>Edit</h1>
                    <div className={styles.formRow}>
                        <label htmlFor="firstName">First Name:</label>
                        <input type="text" id="firstName" 
                            defaultValue={member ? member.getFirstName() : ''}
                            {...register('firstName', { required: true })}
                        />
                    </div>

                    <div className={styles.formRow}>
                        <label htmlFor="lastName">Last Name:</label>
                        <input type="text" id="lastName" 
                            defaultValue={member ? member.getLastName() : ''}
                            {...register('lastName', { required: true })} 
                        />
                    </div>

                    <div className={styles.formRow}>
                        <label htmlFor="organisation">Organisation:</label>
                        <input type="text" id="organisation" 
                            defaultValue={member ? member.getOrganisation() : ''}
                            {...register('organisation')}
                        />
                    </div>

                    <div className={styles.formRow}>
                        <label htmlFor="position">Position:</label>
                        <input type="text" id="position"
                            defaultValue={member ? member.getPosition() : ''}
                            {...register('position')} 
                        />
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
                            defaultValue={member ? member.getEmail() : ''}
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
                            defaultValue={member ? member.getCity() : ''}
                            {...register('city')}
                        />
                    </div>

                    <div className={styles.formRow}>
                        <label htmlFor="mobile">Mobile:</label>
                        <input type="text" id="mobile" 
                            defaultValue={member ? member.getMobile() : ''}
                            {...register('mobile', { pattern: /\d+/ })}
                        />
                    </div>

                    <div className={styles.formRow}>
                        <label htmlFor="postCode">Post Code:</label>
                        <input type="text" id="postCode" 
                            defaultValue={member ? member.getPostCode() : ''}
                            {...register('postCode', { pattern: /\d+/ })}
                        />
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
