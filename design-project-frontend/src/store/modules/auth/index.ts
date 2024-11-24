import { computed, reactive, ref } from 'vue';
import { useRoute } from 'vue-router';
import { defineStore } from 'pinia';
import { useLoading } from '@sa/hooks';
import { SetupStoreId } from '@/enum';
import { useRouterPush } from '@/hooks/common/router';
import { fetchGetUserInfo, fetchLogin } from '@/service/api';
import { localStg } from '@/utils/storage';
import { $t } from '@/locales';
import { useRouteStore } from '../route';
import { useTabStore } from '../tab';
import { clearAuthStorage, getToken } from './shared';

export const useAuthStore = defineStore(SetupStoreId.Auth, () => {
  const route = useRoute();
  const routeStore = useRouteStore();
  const tabStore = useTabStore();
  const { toLogin, redirectFromLogin } = useRouterPush(false);
  const { loading: loginLoading, startLoading, endLoading } = useLoading();

  const token = ref(getToken());

  const userInfo: Api.Auth.UserInfo = reactive({
    userId: '',
    userName: ''
  });

  /** Is login */
  const isLogin = computed(() => Boolean(token.value));

  /** Reset auth store */
  async function resetStore() {
    const authStore = useAuthStore();

    clearAuthStorage();

    authStore.$reset();

    if (!route.meta.constant) {
      await toLogin();
    }

    tabStore.cacheTabs();
    routeStore.resetStore();
  }

  /**
   * Login
   *
   * @param userName User name
   * @param password Password
   * @param [redirect=true] Whether to redirect after login. Default is `true`
   */
  async function login(userName: string, password: string, redirect = true) {
    startLoading();

    try {
      const response = await fetchLogin(userName, password);
      const loginToken = response.data;

      console.log('Login Token:', loginToken); // 调试输出
      localStg.set('token', loginToken);
      const pass = await loginByToken(loginToken);
//

      if (pass) {
        await routeStore.initAuthRoute();

        if (redirect) {
          await redirectFromLogin();
        }

        if (routeStore.isInitAuthRoute) {
          window.$notification?.success({
            message: $t('page.login.common.loginSuccess'),
            description: $t('page.login.common.welcomeBack', { username: userInfo.username })
          });
        }
      }
    } catch (error) {
      alert("用户名或密码错误");
      console.error('Login error:', error);
      resetStore();
    } finally {
      endLoading();
    }
  }


  async function loginByToken(loginToken: Api.Auth.LoginToken) {
    // 1. 存储在本地存储中，后续请求需要它在 headers 中
    // localStg.set('token', loginToken.token);
    localStg.set('refreshToken', loginToken.refreshToken);

    // 2. 获取用户信息
    const pass = await getUserInfo();

    if (pass) {
      token.value = loginToken.token;
      return true;
    }

    return false;
  }

  async function getUserInfo() {
    const { data: info, error } = await fetchGetUserInfo();

    if (!error) {
      // update store
      Object.assign(userInfo, info);

      return true;
    }

    return false;
  }

  async function initUserInfo() {
    const hasToken = getToken();

    if (hasToken) {
      const pass = await getUserInfo();

      if (!pass) {
        resetStore();
      }
    }
  }

  /**
   * Register
   *
   * @param userName User name
   * @param password Password
   * @param email Email
   * @param [redirect=true] Whether to redirect after registration. Default is `true`
   */
  async function register(userName: string, password: string, redirect = true) {
    startLoading();

    const { data, error } = await fetchRegister(userName, password);

    if (!error) {
      if (redirect) {
        await toLogin();
      }
    } else {
      const a = 1;
    }

    endLoading();
  }

  return {
    token,
    userInfo,
    isLogin,
    loginLoading,
    resetStore,
    login,
    initUserInfo,
    register
  };
});
