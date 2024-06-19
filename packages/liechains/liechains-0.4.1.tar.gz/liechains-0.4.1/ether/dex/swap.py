class Swap:
    def quote(self, amount_in) -> int:
        """
        根据token和amount_in报价
        各协议各自实现
        """
        raise NotImplemented
    
    def swap(self, amount_in, min_amount_out):
        """
        执行swap
        """
        raise NotImplemented
