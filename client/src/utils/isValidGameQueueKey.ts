export default function isValidGameQueueKey(value: string) {
  return /^[a-z]{64}$/.test(value);
}
