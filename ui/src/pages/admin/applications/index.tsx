import styles from '@/styles/Table.module.css';
import DataTable from 'react-data-table-component';
import CircularProgress from '@mui/material/CircularProgress';
import useSWR from 'swr'
import { useRouter, NextRouter } from 'next/router';
import { useState } from 'react'
import { deleteApplication, fetchApplications } from '@/lib/api/applications';
import { createMember } from '@/lib/api/membership';
import Applicant from '@/model/applicant';
import SmallButton from '@/components/buttons/SmallButton';
import Member from '@/model/member';
import ErrorComponent from '@/components/Error';

export default function Applications(): JSX.Element {
    const router: NextRouter = useRouter();
    const [errorMessage, setErrorMessage] = useState<string | null>(null);

    const { data, error } = useSWR(['asd'], fetchApplications);

    if (error) return <ErrorComponent message={errorMessage}/>;
    if (!data) return <CircularProgress />;

    const applicantsList: Applicant[] = data.data.data.map((entry: any) => {
        return new Applicant(entry);
    });

    const handleClick: Function = (applicant: Applicant) => {
        router.push({
            pathname: '/admin/applications/review.html',
            query: { data: JSON.stringify(applicant) },
        });
    };

    const approveApplicant: Function = async (applicant: Applicant) => {
        const newMember = new Member(applicant);
        const membershipResponse = await createMember(newMember, true);

        if (membershipResponse.status !== 200) {
            setErrorMessage(membershipResponse.data.message);
            return;
        }

        const applicationResponse = await deleteApplication(applicant.getId())

        if (applicationResponse.status !== 200) {
            setErrorMessage(applicationResponse.data.message);
            return
        }

        router.reload();
    }

    const rejectApplicant: Function = async (id: string) => {
        const response = await deleteApplication(id, true);

        if (response.status !== 200) {
            setErrorMessage(response.data.message);
            return;
        }
        
        router.reload();
    }

    const columns = [
        {
            name: 'First Name',
            selector: (row: Applicant) => row.getFirstName(),
            sortable: true,
        },
        {
            name: 'Last Name',
            selector: (row: Applicant) => row.getLastName(),
            sortable: true,
        },
        {
            name: 'Organisation',
            selector: (row: Applicant) => row.getOrganisation(),
        },
        {
            name: 'Position',
            selector: (row: Applicant) => row.getPosition(),
        },
        {
            name: 'Email',
            selector: (row: Applicant) => row.getEmail(),
        },
        {
            name: 'DOB',
            selector: (row: Applicant) => row.getDOB().format('LL'),
        },
        {
            name: 'City',
            selector: (row: Applicant) => row.getCity(),
        },
        {
            button: true,
            cell: (row: Applicant) => <SmallButton handler={approveApplicant} data={row} type='approve'/> 
        },
        {
            button: true,
            cell: (row: Applicant) => <SmallButton handler={rejectApplicant} data={row.getId()} type='reject'/>
        }
    ];

    return (
        <>
            {errorMessage && <ErrorComponent message={errorMessage}/>}
            <main className={styles.tableContainer}>
                <div className={styles.table}>
                    <DataTable
                        title="Applications"
                        columns={columns}
                        data={applicantsList}
                        onRowClicked={(row) => handleClick(row)}
                        pagination
                        paginationRowsPerPageOptions={[10, 25, 50, 100]}
                        pointerOnHover
                        highlightOnHover
                        striped
                        responsive
                    />
                </div>
            </main>
        </>
    )
}
