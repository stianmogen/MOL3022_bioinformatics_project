import { API_URL } from '~/constant';
import type { HTTPError, Options } from 'ky';
import ky from 'ky';

import type { ActionResponse } from '~/types';


export type HttpRequestOptions = {
  baseUrl?: string;
};

export class HttpRequest {
  url: string;
  withAuth: boolean;
  request: Request;
  api: typeof ky;

  constructor(url: string, request: Request, withAuth = true, options: HttpRequestOptions = {}) {
    this.url = url;
    this.request = request;
    this.withAuth = withAuth;

    this.api = ky.create({ prefixUrl: options?.baseUrl || API_URL });
  }
  async #getHeaders(): Promise<Headers> {
    const headers = new Headers();
    return headers;
  }


  async #handleRequestError(error: Error) {
      console.log(error);
    if (error.name === 'HTTPError') {
      const httpError = error as HTTPError;
      const errorJson = (await httpError.response.json()) as Omit<ActionResponse, 'ok'> | undefined;
      if (typeof errorJson?.detail === 'string' || typeof errorJson?.violations === 'object') {
        return Promise.reject({
          ok: false,
          detail: errorJson.detail || undefined,
          violations: errorJson.violations || undefined,
        } as ActionResponse);
      }
      return Promise.reject({ ok: false, detail: `${httpError.response.status} - ${httpError.response.statusText}` } as ActionResponse);
    }
    if (error.message) {
      return Promise.reject({ ok: false, detail: error.message });
    }
    return Promise.reject({ ok: false, detail: 'Something went wrong' });
  }

  async get<ReturnType>(searchParams?: URLSearchParams) {
    return this.fetch<ReturnType>({ method: 'get', searchParams });
  }

  async post<ReturnType>(data?: unknown) {
    return this.fetch<ReturnType>({ method: 'post', json: data });
  }

  async put<ReturnType>(data?: unknown) {
    return this.fetch<ReturnType>({ method: 'put', json: data });
  }

  async delete<ReturnType>() {
    return this.fetch<ReturnType>({ method: 'delete' });
  }

  async fetch<ReturnType>(options?: Options) {
    return this.api(this.url, {
        headers: await this.#getHeaders(),
      ...options,
    })
      .json<ReturnType>()
      .catch(this.#handleRequestError);
  }
}
