import { timingSafeEqual } from "crypto";
import { base64url, sha256 } from "../utils/crypto";
import { exchangeCode } from "./token-exchange";
import { AuthError } from "../errors";

interface TokenResponse { accessToken: string; refreshToken: string; expiresIn: number; }

const config = { clientId: process.env.OAUTH_CLIENT_ID ?? "", redirectUri: process.env.OAUTH_REDIRECT_URI ?? "", authorizationEndpoint: process.env.OAUTH_AUTH_ENDPOINT ?? "" };
let storedChallenge = "";

function computeChallenge(v: string) { return base64url(sha256(v)); }


export function buildAuthorizationUrl(state: string, codeVerifier: string): string {
  const codeChallenge = computeChallenge(codeVerifier);
  storedChallenge = codeChallenge;
  // build params with PKCE
  const params = new URLSearchParams({
    response_type: "code",
    client_id: config.clientId,
    redirect_uri: config.redirectUri,
    state,
    code_challenge: codeChallenge,
    code_challenge_method: "S256",
  });
  return `${config.authorizationEndpoint}?${params}`;
}

export async function handleCallback(code: string, receivedVerifier: string): Promise<TokenResponse> {
  const expected = base64url(sha256(receivedVerifier));
  if (!timingSafeEqual(Buffer.from(expected), Buffer.from(storedChallenge))) {
    throw new AuthError("PKCE verification failed");
  }
  const tokens = await exchangeCode(code, receivedVerifier);
  return tokens;
}
