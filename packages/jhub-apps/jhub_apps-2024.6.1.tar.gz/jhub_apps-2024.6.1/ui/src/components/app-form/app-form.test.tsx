import { app, environments, frameworks, profiles } from '@src/data/api';
import { currentUser } from '@src/data/user';
import axios from '@src/utils/axios';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import '@testing-library/jest-dom';
import { act, fireEvent, render } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import MockAdapter from 'axios-mock-adapter';
import { BrowserRouter } from 'react-router-dom';
import { RecoilRoot } from 'recoil';
import { currentUser as defaultUser } from '../../store';
import AppForm from './app-form';

describe('AppForm', () => {
  Object.defineProperty(URL, 'createObjectURL', {
    writable: true,
    value: jest.fn(),
  });

  const queryClient = new QueryClient();
  const mock = new MockAdapter(axios);
  beforeAll(() => {
    mock.reset();
  });

  beforeEach(() => {
    queryClient.clear();
    mock.reset();
  });

  test('renders successfully', () => {
    const { baseElement } = render(
      <RecoilRoot>
        <QueryClientProvider client={queryClient}>
          <BrowserRouter>
            <AppForm />
          </BrowserRouter>
        </QueryClientProvider>
      </RecoilRoot>,
    );
    expect(baseElement.querySelector('#app-form')).toBeTruthy();
  });

  test('simulates creating a standard app', async () => {
    mock.onGet(new RegExp('/frameworks')).reply(200, frameworks);
    mock.onPost(new RegExp('/server')).reply(200);
    queryClient.setQueryData(['app-frameworks'], frameworks);
    queryClient.setQueryData(['app-environments'], null);
    queryClient.setQueryData(['app-profiles'], null);
    const { baseElement } = render(
      <RecoilRoot initializeState={({ set }) => set(defaultUser, currentUser)}>
        <QueryClientProvider client={queryClient}>
          <BrowserRouter>
            <AppForm />
          </BrowserRouter>
        </QueryClientProvider>
      </RecoilRoot>,
    );

    const displayNameField = baseElement.querySelector(
      '#display_name',
    ) as HTMLInputElement;
    const frameworkField = baseElement.querySelector(
      '[name="framework"]',
    ) as HTMLSelectElement;
    const envVariableField = baseElement.querySelector(
      '#env',
    ) as HTMLInputElement;
    if (displayNameField && frameworkField && envVariableField) {
      // Attempt submitting without filling in required fields
      const btn = baseElement.querySelector('#submit-btn') as HTMLButtonElement;
      expect(btn).toBeInTheDocument();
      expect(btn).toHaveTextContent('Create App');
      expect(btn).not.toHaveAttribute('disabled', 'disabled');
      await act(async () => {
        btn.click();
      });

      await userEvent.type(displayNameField, 'App 1');
      fireEvent.change(frameworkField, { target: { value: 'panel' } });

      // prettier-ignore
      const envJson = JSON.stringify({ "KEY": "VALUE", "KEY-1": "Value-1" });
      fireEvent.change(envVariableField, { target: { value: envJson } });

      // Submit with all required fields filled in
      await act(async () => {
        btn.click();
      });
      // TODO: Update this test when everything is running in single react app
      expect(window.location.pathname).not.toBe('/create-app');
    }
  });

  test('simulates creating a standard app with thumbnail', async () => {
    mock.onGet(new RegExp('/frameworks')).reply(200, frameworks);
    mock.onPost(new RegExp('/server')).reply(200);
    queryClient.setQueryData(['app-frameworks'], frameworks);
    queryClient.setQueryData(['app-environments'], null);
    queryClient.setQueryData(['app-profiles'], null);
    const { baseElement } = render(
      <RecoilRoot>
        <QueryClientProvider client={queryClient}>
          <BrowserRouter>
            <AppForm />
          </BrowserRouter>
        </QueryClientProvider>
      </RecoilRoot>,
    );

    const displayNameField = baseElement.querySelector(
      '#display_name',
    ) as HTMLInputElement;
    const thumbnailField = baseElement.querySelector(
      '#thumbnail',
    ) as HTMLInputElement;
    const frameworkField = baseElement.querySelector(
      '[name="framework"]',
    ) as HTMLSelectElement;
    if (displayNameField && thumbnailField && frameworkField) {
      // Attempt submitting without filling in required fields
      const btn = baseElement.querySelector('#submit-btn') as HTMLButtonElement;
      expect(btn).toBeInTheDocument();
      expect(btn).toHaveTextContent('Create App');
      expect(btn).not.toHaveAttribute('disabled', 'disabled');
      await act(async () => {
        btn.click();
      });

      const file = new File(['File contents'], 'image.png', {
        type: 'image/png',
      });
      await userEvent.upload(thumbnailField, file);

      await userEvent.type(displayNameField, 'App 1');
      fireEvent.change(frameworkField, { target: { value: 'panel' } });

      // Submit with all required fields filled in
      await act(async () => {
        btn.click();
      });
      // TODO: Update this test when everything is running in single react app
      expect(window.location.pathname).not.toBe('/create-app');
    }
  });

  test('simulates creating an app with additional fields', async () => {
    mock.onGet(new RegExp('/frameworks')).reply(200, frameworks);
    mock.onGet(new RegExp('/conda-environments')).reply(200, environments);
    mock.onGet(new RegExp('/spawner-profiles')).reply(200, profiles);
    mock.onPost(new RegExp('/server')).reply(200);
    queryClient.setQueryData(['app-frameworks'], frameworks);
    queryClient.setQueryData(['app-environments'], environments);
    queryClient.setQueryData(['app-profiles'], profiles);
    const { baseElement } = render(
      <RecoilRoot>
        <QueryClientProvider client={queryClient}>
          <BrowserRouter>
            <AppForm />
          </BrowserRouter>
        </QueryClientProvider>
      </RecoilRoot>,
    );

    const displayNameField = baseElement.querySelector(
      '#display_name',
    ) as HTMLInputElement;
    const descriptionField = baseElement.querySelector(
      '#description',
    ) as HTMLInputElement;
    const frameworkField = baseElement.querySelector(
      '#framework',
    ) as HTMLSelectElement;
    const environmentField = baseElement.querySelector(
      '#conda_env',
    ) as HTMLSelectElement;
    const profileField = baseElement.querySelector(
      '#profile',
    ) as HTMLSelectElement;
    const customCommandField = baseElement.querySelector(
      '#custom_command',
    ) as HTMLInputElement;
    if (
      displayNameField &&
      descriptionField &&
      frameworkField &&
      environmentField &&
      profileField &&
      customCommandField
    ) {
      // Attempt submitting without filling in required fields
      const btn = baseElement.querySelector('#submit-btn') as HTMLButtonElement;
      expect(btn).toBeInTheDocument();
      expect(btn).toHaveTextContent('Create App');
      expect(btn).not.toHaveAttribute('disabled', 'disabled');
      await act(async () => {
        btn.click();
      });

      await userEvent.type(displayNameField, 'App 1');
      await userEvent.type(descriptionField, 'Some App');
      await act(async () => {
        fireEvent.change(frameworkField, { target: { value: 'custom' } });
      });
      await act(async () => {
        fireEvent.change(environmentField, { target: { value: 'env-1' } });
      });
      await act(async () => {
        fireEvent.change(profileField, { target: { value: 'Small' } });
      });
      await userEvent.type(customCommandField, 'Some command');

      // Submit with all required fields filled in
      await act(async () => {
        btn.click();
      });
      // TODO: Update this test when everything is running in single react app
      expect(window.location.pathname).not.toBe('/create-app');
    }
  });

  test('simulates creating an app with an error', async () => {
    mock.onGet(new RegExp('/frameworks')).reply(200, frameworks);
    mock.onPost(new RegExp('/server')).reply(500, { message: 'Some error' });
    const { baseElement } = render(
      <RecoilRoot>
        <QueryClientProvider client={queryClient}>
          <BrowserRouter>
            <AppForm />
          </BrowserRouter>
        </QueryClientProvider>
      </RecoilRoot>,
    );

    const displayNameField = baseElement.querySelector(
      '#display_name',
    ) as HTMLInputElement;
    const descriptionField = baseElement.querySelector(
      '#description',
    ) as HTMLInputElement;
    const frameworkField = baseElement.querySelector(
      '[name="framework"]',
    ) as HTMLSelectElement;
    if (displayNameField && descriptionField && frameworkField) {
      await userEvent.type(displayNameField, 'App 1');
      await userEvent.type(descriptionField, 'Some App');
      fireEvent.change(frameworkField, { target: { value: 'panel' } });

      const btn = baseElement.querySelector('#submit-btn') as HTMLButtonElement;
      expect(btn).toBeInTheDocument();
      expect(btn).toHaveTextContent('Create App');
      expect(btn).not.toHaveAttribute('disabled', 'disabled');
      await act(async () => {
        btn.click();
      });
      // TODO: Update this test when everything is running in single react app
      expect(window.location.pathname).not.toBe('/create-app');
    }
  });

  test('simulates editing an app', async () => {
    mock.onGet(new RegExp('/frameworks')).reply(200, frameworks);
    mock.onGet(new RegExp('/server/app-1')).reply(200, app);
    queryClient.setQueryData(['app-form'], app);
    queryClient.setQueryData(['app-frameworks'], frameworks);
    queryClient.setQueryData(['app-environments'], null);
    queryClient.setQueryData(['app-profiles'], null);
    mock.onPut().reply(200);
    const { baseElement } = render(
      <RecoilRoot>
        <QueryClientProvider client={queryClient}>
          <BrowserRouter>
            <AppForm id="app-1" />
          </BrowserRouter>
        </QueryClientProvider>
      </RecoilRoot>,
    );

    const displayNameField = baseElement.querySelector(
      '#display_name',
    ) as HTMLInputElement;
    const descriptionField = baseElement.querySelector(
      '#description',
    ) as HTMLInputElement;
    const frameworkField = baseElement.querySelector(
      '[name="framework"]',
    ) as HTMLSelectElement;
    if (displayNameField && descriptionField && frameworkField) {
      await userEvent.type(displayNameField, 'App 1');
      await userEvent.type(descriptionField, 'Some App');
      fireEvent.change(frameworkField, { target: { value: 'panel' } });

      const btn = baseElement.querySelector('#submit-btn') as HTMLButtonElement;
      expect(btn).toBeInTheDocument();
      expect(btn).toHaveTextContent('Save');
      expect(btn).not.toHaveAttribute('disabled', 'disabled');
      await act(async () => {
        btn.click();
      });
      // TODO: Update this test when everything is running in single react app
      expect(window.location.pathname).not.toBe('/edit-app');
    }
  });

  test('simulates editing an app with an error', async () => {
    mock.onGet(new RegExp('/frameworks')).reply(200, frameworks);
    mock.onGet(new RegExp('/server/app-1')).reply(200, app);
    mock
      .onPut(new RegExp('/server/app-1'))
      .reply(500, { message: 'Some error' });
    const { baseElement } = render(
      <RecoilRoot>
        <QueryClientProvider client={queryClient}>
          <BrowserRouter>
            <AppForm id="app-1" />
          </BrowserRouter>
        </QueryClientProvider>
      </RecoilRoot>,
    );

    const displayNameField = baseElement.querySelector(
      '#display_name',
    ) as HTMLInputElement;
    const descriptionField = baseElement.querySelector(
      '#description',
    ) as HTMLInputElement;
    const frameworkField = baseElement.querySelector(
      '[name="framework"]',
    ) as HTMLSelectElement;
    if (displayNameField && descriptionField && frameworkField) {
      await userEvent.type(displayNameField, 'App 1');
      await userEvent.type(descriptionField, 'Some App');
      fireEvent.change(frameworkField, { target: { value: 'panel' } });

      const btn = baseElement.querySelector('#submit-btn') as HTMLButtonElement;
      expect(btn).toBeInTheDocument();
      expect(btn).toHaveTextContent('Save');
      expect(btn).not.toHaveAttribute('disabled', 'disabled');
      await act(async () => {
        btn.click();
      });
      // TODO: Update this test when everything is running in single react app
      expect(window.location.pathname).not.toBe('/edit-app');
    }
  });

  test('clicks cancel to home', async () => {
    mock.onGet(new RegExp('/frameworks')).reply(200, frameworks);
    mock.onGet(new RegExp('/server/app-1')).reply(200, app);
    const { baseElement } = render(
      <RecoilRoot>
        <QueryClientProvider client={queryClient}>
          <BrowserRouter>
            <AppForm />
          </BrowserRouter>
        </QueryClientProvider>
      </RecoilRoot>,
    );
    const btn = baseElement.querySelector('#cancel-btn') as HTMLButtonElement;
    expect(btn).toBeInTheDocument();
    expect(btn).toHaveTextContent('Cancel');
    expect(btn).not.toHaveAttribute('disabled', 'disabled');
    await act(async () => {
      btn.click();
    });
    expect(window.location.pathname).toBe('/');
  });
});
