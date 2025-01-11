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

      console.log('Login Token:', loginToken);

      // 存储 token
      localStg.set('token', loginToken);
      token.value = loginToken.token;

      const pass = await loginByToken(loginToken);

      if (pass) {
        await routeStore.initAuthRoute();

        if (routeStore.isInitAuthRoute) {
          window.$notification?.success({
            message: $t('page.login.common.loginSuccess'),
            description: $t('page.login.common.welcomeBack', { username: userInfo.username })
          });
        }

        // 登录成功后刷新页面
        if (redirect) {
          // 等待通知显示完成后再刷新
          setTimeout(() => {
            window.location.reload();
          }, 1000);
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
    // 先更新响应式引用
    token.value = loginToken.token;

    // 再存储到 localStorage
    localStg.set('refreshToken', loginToken.refreshToken);

    // 获取用户信息
    const pass = await getUserInfo();

    // 再次确保 token 是最新的
    if (pass) {
      token.value = loginToken.token;
    }

    return pass;
  }

  async function getUserInfo() {
    const { data: info, error } = await fetchGetUserInfo();

    if (!error) {
      // 使用解构赋值来触发响应式更新
      const { userId, userName, username } = info;

      // 逐个更新响应式属性
      userInfo.userId = userId;
      userInfo.userName = userName;
      userInfo.username = username;

      // 强制更新 token 以触发 isLogin 的重新计算
      token.value = token.value;

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
