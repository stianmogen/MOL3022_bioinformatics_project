import type { ActionArgs } from '@remix-run/node';
import { useActionData } from '@remix-run/react';


export const action = async ({ request, params }: ActionArgs) => {
      const formData = await request.formData();
      if (request.method === 'POST') {
          const res = await fetch('http://localhost:8000/', {
              method: 'POST',
              body: JSON.stringify({ "string":formData.get("sequence") })
          })
          return res.json();
      }

};
export default function Index() {
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
        { actionData?.data && <div>{actionData.data}</div>}
    </div>

  );
}
