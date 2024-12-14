package com.kclgroup.backend.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.kclgroup.backend.pojo.entity.StockKline;
import com.kclgroup.backend.pojo.vo.KlineVo;
import org.apache.ibatis.annotations.Select;

import java.util.List;

public interface StockKlineMapper extends BaseMapper<StockKline> {
    @Select("select stock_code,date_time,open_price,close_price,high_price,low_price,volume,trade_value,amplitude,up_down_range,up_down_price,turnover_rate from stock_kline where stock_code = #{stockCode}")
    List<KlineVo> getStockKline(String stockCode);
}
