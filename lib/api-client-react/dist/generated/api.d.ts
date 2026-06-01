import type { QueryKey, UseMutationOptions, UseMutationResult, UseQueryOptions, UseQueryResult } from '@tanstack/react-query';
import type { BotStatus, DiscordUser, ErrorResponse, GetMinecraftStatusParams, Guild, GuildSettings, GuildSettingsInput, HealthStatus, MinecraftStatus, SuccessResponse } from './api.schemas';
import { customFetch } from '../custom-fetch';
import type { ErrorType, BodyType } from '../custom-fetch';
type AwaitedInput<T> = PromiseLike<T> | T;
type Awaited<O> = O extends AwaitedInput<infer T> ? T : never;
type SecondParameter<T extends (...args: never) => unknown> = Parameters<T>[1];
export declare const getHealthCheckUrl: () => string;
/**
 * @summary Health check
 */
export declare const healthCheck: (options?: RequestInit) => Promise<HealthStatus>;
export declare const getHealthCheckQueryKey: () => readonly ["/api/healthz"];
export declare const getHealthCheckQueryOptions: <TData = Awaited<ReturnType<typeof healthCheck>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof healthCheck>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof healthCheck>>, TError, TData> & {
    queryKey: QueryKey;
};
export type HealthCheckQueryResult = NonNullable<Awaited<ReturnType<typeof healthCheck>>>;
export type HealthCheckQueryError = ErrorType<unknown>;
/**
 * @summary Health check
 */
export declare function useHealthCheck<TData = Awaited<ReturnType<typeof healthCheck>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof healthCheck>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
export declare const getGetMeUrl: () => string;
/**
 * @summary Get current authenticated user
 */
export declare const getMe: (options?: RequestInit) => Promise<DiscordUser>;
export declare const getGetMeQueryKey: () => readonly ["/api/auth/me"];
export declare const getGetMeQueryOptions: <TData = Awaited<ReturnType<typeof getMe>>, TError = ErrorType<ErrorResponse>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getMe>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof getMe>>, TError, TData> & {
    queryKey: QueryKey;
};
export type GetMeQueryResult = NonNullable<Awaited<ReturnType<typeof getMe>>>;
export type GetMeQueryError = ErrorType<ErrorResponse>;
/**
 * @summary Get current authenticated user
 */
export declare function useGetMe<TData = Awaited<ReturnType<typeof getMe>>, TError = ErrorType<ErrorResponse>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getMe>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
export declare const getLogoutUrl: () => string;
/**
 * @summary Logout current user
 */
export declare const logout: (options?: RequestInit) => Promise<SuccessResponse>;
export declare const getLogoutMutationOptions: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof logout>>, TError, void, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationOptions<Awaited<ReturnType<typeof logout>>, TError, void, TContext>;
export type LogoutMutationResult = NonNullable<Awaited<ReturnType<typeof logout>>>;
export type LogoutMutationError = ErrorType<unknown>;
/**
* @summary Logout current user
*/
export declare const useLogout: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof logout>>, TError, void, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationResult<Awaited<ReturnType<typeof logout>>, TError, void, TContext>;
export declare const getGetUserGuildsUrl: () => string;
/**
 * @summary Get guilds where user has manage permissions and bot is present
 */
export declare const getUserGuilds: (options?: RequestInit) => Promise<Guild[]>;
export declare const getGetUserGuildsQueryKey: () => readonly ["/api/auth/guilds"];
export declare const getGetUserGuildsQueryOptions: <TData = Awaited<ReturnType<typeof getUserGuilds>>, TError = ErrorType<ErrorResponse>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getUserGuilds>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof getUserGuilds>>, TError, TData> & {
    queryKey: QueryKey;
};
export type GetUserGuildsQueryResult = NonNullable<Awaited<ReturnType<typeof getUserGuilds>>>;
export type GetUserGuildsQueryError = ErrorType<ErrorResponse>;
/**
 * @summary Get guilds where user has manage permissions and bot is present
 */
export declare function useGetUserGuilds<TData = Awaited<ReturnType<typeof getUserGuilds>>, TError = ErrorType<ErrorResponse>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getUserGuilds>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
export declare const getGetBotStatusUrl: () => string;
/**
 * @summary Get bot online status and stats
 */
export declare const getBotStatus: (options?: RequestInit) => Promise<BotStatus>;
export declare const getGetBotStatusQueryKey: () => readonly ["/api/bot/status"];
export declare const getGetBotStatusQueryOptions: <TData = Awaited<ReturnType<typeof getBotStatus>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getBotStatus>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof getBotStatus>>, TError, TData> & {
    queryKey: QueryKey;
};
export type GetBotStatusQueryResult = NonNullable<Awaited<ReturnType<typeof getBotStatus>>>;
export type GetBotStatusQueryError = ErrorType<unknown>;
/**
 * @summary Get bot online status and stats
 */
export declare function useGetBotStatus<TData = Awaited<ReturnType<typeof getBotStatus>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getBotStatus>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
export declare const getGetMinecraftStatusUrl: (params: GetMinecraftStatusParams) => string;
/**
 * @summary Check Minecraft server status
 */
export declare const getMinecraftStatus: (params: GetMinecraftStatusParams, options?: RequestInit) => Promise<MinecraftStatus>;
export declare const getGetMinecraftStatusQueryKey: (params?: GetMinecraftStatusParams) => readonly ["/api/minecraft/status", ...GetMinecraftStatusParams[]];
export declare const getGetMinecraftStatusQueryOptions: <TData = Awaited<ReturnType<typeof getMinecraftStatus>>, TError = ErrorType<unknown>>(params: GetMinecraftStatusParams, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getMinecraftStatus>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof getMinecraftStatus>>, TError, TData> & {
    queryKey: QueryKey;
};
export type GetMinecraftStatusQueryResult = NonNullable<Awaited<ReturnType<typeof getMinecraftStatus>>>;
export type GetMinecraftStatusQueryError = ErrorType<unknown>;
/**
 * @summary Check Minecraft server status
 */
export declare function useGetMinecraftStatus<TData = Awaited<ReturnType<typeof getMinecraftStatus>>, TError = ErrorType<unknown>>(params: GetMinecraftStatusParams, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getMinecraftStatus>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
export declare const getGetGuildSettingsUrl: (guildId: string) => string;
/**
 * @summary Get bot settings for a guild
 */
export declare const getGuildSettings: (guildId: string, options?: RequestInit) => Promise<GuildSettings>;
export declare const getGetGuildSettingsQueryKey: (guildId: string) => readonly [`/api/settings/${string}`];
export declare const getGetGuildSettingsQueryOptions: <TData = Awaited<ReturnType<typeof getGuildSettings>>, TError = ErrorType<ErrorResponse>>(guildId: string, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getGuildSettings>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof getGuildSettings>>, TError, TData> & {
    queryKey: QueryKey;
};
export type GetGuildSettingsQueryResult = NonNullable<Awaited<ReturnType<typeof getGuildSettings>>>;
export type GetGuildSettingsQueryError = ErrorType<ErrorResponse>;
/**
 * @summary Get bot settings for a guild
 */
export declare function useGetGuildSettings<TData = Awaited<ReturnType<typeof getGuildSettings>>, TError = ErrorType<ErrorResponse>>(guildId: string, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getGuildSettings>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
export declare const getUpdateGuildSettingsUrl: (guildId: string) => string;
/**
 * @summary Update bot settings for a guild
 */
export declare const updateGuildSettings: (guildId: string, guildSettingsInput: GuildSettingsInput, options?: RequestInit) => Promise<GuildSettings>;
export declare const getUpdateGuildSettingsMutationOptions: <TError = ErrorType<ErrorResponse>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof updateGuildSettings>>, TError, {
        guildId: string;
        data: BodyType<GuildSettingsInput>;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationOptions<Awaited<ReturnType<typeof updateGuildSettings>>, TError, {
    guildId: string;
    data: BodyType<GuildSettingsInput>;
}, TContext>;
export type UpdateGuildSettingsMutationResult = NonNullable<Awaited<ReturnType<typeof updateGuildSettings>>>;
export type UpdateGuildSettingsMutationBody = BodyType<GuildSettingsInput>;
export type UpdateGuildSettingsMutationError = ErrorType<ErrorResponse>;
/**
* @summary Update bot settings for a guild
*/
export declare const useUpdateGuildSettings: <TError = ErrorType<ErrorResponse>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof updateGuildSettings>>, TError, {
        guildId: string;
        data: BodyType<GuildSettingsInput>;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationResult<Awaited<ReturnType<typeof updateGuildSettings>>, TError, {
    guildId: string;
    data: BodyType<GuildSettingsInput>;
}, TContext>;
export {};
//# sourceMappingURL=api.d.ts.map