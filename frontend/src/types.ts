export interface Email {
    id: string;
    from: string; 
    patient_name: string;
    subject: string;
    body: string;
    reply?: string; // optional, only used when sending
  }