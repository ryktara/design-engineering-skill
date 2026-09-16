import { error } from '@sveltejs/kit';
import { patientById, visits, invoices } from '$lib/data/sample';
import type { PageLoad } from './$types';

export const load: PageLoad = ({ params }) => {
  const patient = patientById(params.id);
  if (!patient) error(404, 'Patient not found');
  return {
    patient,
    visits: visits.filter((v) => v.patientId === patient.id),
    invoices: invoices.filter((i) => i.patientId === patient.id)
  };
};
