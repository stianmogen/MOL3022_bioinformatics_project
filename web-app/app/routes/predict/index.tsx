import type { ActionArgs } from '@remix-run/node';
import { useActionData } from '@remix-run/react';
import { PREDICTION_API } from '~/api/predict.server';
import type{ PredictionRequest } from '~/types';
import { API_URL } from '~/constant';


export const action = async ({ request, params }: ActionArgs) => {
    const formData = await request.formData()
    if (request.method == "POST") {
        var myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");

        const raw = JSON.stringify({
          "sequence": formData.get("sequence")
        });

        return fetch(`${API_URL}predict`, {
          method: 'POST',
          headers: myHeaders,
          body: raw,
          redirect: 'follow'
        })
    }

};
export default function Predict() {
    const actionData = useActionData<typeof action>();
  return (
    <div>
        <h1> Input the a protein sequence</h1>
        <form method='post'>

        <label className='mb-2 italic' htmlFor='company'>
              Sequence
            </label>
            <input
              className='block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:focus:border-blue-500 dark:focus:ring-blue-500'
              defaultValue={""}
              id='sequence'
              name='sequence'
              required
              type='text'
            />
        <button type="submit">Predict</button>
        </form>
        { actionData?.ans && <div>{actionData?.ans}</div>}
    </div>

  );
}

