import { DATE_FORMAT, TIMESTAMP_FORMAT } from '@/lib/constants';
import dayjs from 'dayjs';

class Applicant {
    private readonly id: number
    private readonly firstName: string;
    private readonly lastName: string;
    private readonly organisation: string;
    private readonly position: string;
    private readonly industry: string;
    private readonly email: string;
    private readonly dob: string;
    private readonly city: string;
    private readonly mobile: string;
    private readonly postCode: string;
    private readonly createdAt: string;

    constructor(props: any) {
        this.id = props.id
        this.firstName = props.firstName;
        this.lastName = props.lastName;
        this.organisation = props.organisation;
        this.position = props.position;
        this.industry = props.industry;
        this.email = props.email;
        this.dob = props.dob;
        this.city = props.city;
        this.mobile = props.mobile;
        this.postCode = props.postCode;
        this.createdAt = dayjs(props.createdAt).format(TIMESTAMP_FORMAT);
    }

    getId() {
        return this.id;
    }

    getFirstName() {
        return this.firstName;
    }
    
    getLastName() {
        return this.lastName;
    }
    
    getOrganisation() {
        return this.organisation;
    }
    
    getPosition() {
        return this.position;
    }
    
    getIndustry() {
        return this.industry;
    }
    
    getEmail() {
        return this.email;
    }
    
    getDOB() {
        return dayjs(this.dob, DATE_FORMAT);
    }

    getCity() {
        return this.city;
    }
    
    getMobile() {
        return this.mobile;
    }
    
    getPostCode() {
        return this.postCode;
    }

    getCreatedAt() {
        return this.createdAt;
    }
}

export default Applicant
