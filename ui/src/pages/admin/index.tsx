import styles from '@/styles/Table.module.css';
import DataTable from 'react-data-table-component';
import useSWR, {SWRResponse} from 'swr'
import dayjs from 'dayjs';
import CircularProgress from '@mui/material/CircularProgress';
import { useRouter, NextRouter } from 'next/router';
import { useState, useEffect } from 'react';
import Member from '@/model/member';
import { fetchMembers, deleteMember } from '@/lib/api/membership';
import TableSubHeaderComponent from '@/components/TableSubHeader';
import SmallButton from '@/components/buttons/SmallButton';
import ErrorComponent from '@/components/Error';

export default function Applications() {
    const router: NextRouter = useRouter()
    const [initMembers, setMembers] = useState(null);
    const [filteredMembers, setFilteredMembers] = useState(null);
    const [filterText, setFilterText] = useState<string>('');
    const [errorMessage, setErrorMessage] = useState<string | null>(null);

    useEffect(() => {
        if(initMembers) {
            setFilteredMembers(initMembers.filter((member: Member) => member.identify(filterText)));
        }
    }, [filterText, initMembers])

    const { data, error }: SWRResponse = useSWR(['asd'], fetchMembers)

    if (error) return <ErrorComponent message={errorMessage}/>;
    if (!data) return <CircularProgress />;

    if (!initMembers) {
        const membersList: Member[] = data?.data.data.map((entry: Member) => {
            return new Member(entry);
        });
        setMembers(membersList.sort((memberA, memberB) => memberA.compare(memberB)));
    }
    
    const handleClick: Function = (member: Member) => {
        router.push({
            pathname: '/admin/member/edit.html',
            query: { data: JSON.stringify(member) },
        });
    };

    const handleDelete: Function = async (row: Member) => {
        if(confirm(`Are you sure you want to delete ${row.getName()}?`)) {
            const response = await deleteMember(row.getId().toString());
            if(response.status !== 200) {
                setErrorMessage(response.data.message);
                return;
            }
    
            router.reload();
        }
    }

    const columns = [
        {
            name: 'Name',
            selector: (row: Member) => row.getName(),
            sortable: true,
        },
        {
            name: 'Organisation',
            selector: (row: Member) => row.getOrganisation(),
        },
        {
            name: 'Position',
            selector: (row: Member) => row.getPosition(),
        },
        {
            name: 'Email',
            selector: (row: Member) => row.getEmail(),
        },
        {
            name: 'DOB',
            selector: (row: Member) => row.getDOB(),
            sortable: true
        },
        {
            name: 'Date Created',
            selector: (row: Member) => row.getDateCreated(),
            sortable: true
        },
        {
            button: true,
            cell: (row: Member) => <SmallButton handler={handleDelete} data={row} type='reject' />
        }
    ];

    return (
        <>
            {errorMessage && <ErrorComponent message={errorMessage}/>}
            <main className={styles.tableContainer}>
                <div className={styles.table}>
                    <DataTable
                        title='Members'
                        columns={columns}
                        data={filteredMembers || initMembers}
                        onRowClicked={(row) => handleClick(row)}
                        pagination
                        paginationRowsPerPageOptions={[10, 25, 50, 100]}
                        pointerOnHover
                        highlightOnHover
                        striped
                        responsive
                        subHeader
                        subHeaderComponent={<TableSubHeaderComponent onFilter={setFilterText} data={initMembers} />}
                    />
                </div>
            </main>
        </>
    )
}
