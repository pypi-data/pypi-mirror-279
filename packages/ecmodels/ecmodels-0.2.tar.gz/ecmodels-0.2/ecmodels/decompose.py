import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import islice

def chetverikov_decompose(seq, n):
    def preliminary_trend_assessment(seq, n, next = False):
      def window(seq, n=2):
          it = iter(seq)
          res = tuple(islice(it, n))
          if len(res) == n:
              yield res
          for elem in it:
              res = res[1:] + (elem,)
              yield res

      a = np.array(seq)
      chron = []

      for i in window(a, n + 1):
          g = np.array(i)
          g[0] = g[0] / 2
          g[-1] = g[-1] /2
          chron.append(g.mean())
      if next:
          return chron
      else:
          return chron

    def first_seasonal_assessment(seq, n, next = False, previous = preliminary_trend_assessment):
      def split_sequence(sequence, period):
          it = iter(sequence)
          while True:
              chunk = tuple(islice(it, period))
              if not chunk:
                  return
              yield np.array(chunk)

      n_ = int(n / 2)
      chron = previous(seq, n, next = True)
      l = seq[n_:-n_] - chron

      rows_to_exclude = []
      rows_to_exclude.extend(l[:n_].index.values)
      rows_to_exclude.extend(l[-n_ + 1:].index.values)
      subsequences = list(split_sequence(l[~l.index.isin(rows_to_exclude)], n))

      years_std = [l[:n_].std(ddof=1)]

      for i in subsequences:
          years_std.append(i.std(ddof=1))

      years_std.append(l[-n_ + 1:].std(ddof=1))
      years = [np.array(l[:n_]), *subsequences, np.array(l[-n_ + 1:])]
      n_years = len(years)
      l_tilda = np.hstack(np.array(years, dtype=object) / years_std)
      l_tilda_years = np.array(years, dtype=object) / years_std
      padded_arrays = [np.pad(arr, (0, n - len(arr)), 'constant') for arr in l_tilda_years]
      V1 = np.vstack(padded_arrays).mean(axis=0)
      if next:
          return V1, n_years, years_std
      else:
          return V1

    def first_trend_assessment(seq, n, next = False, previous = first_seasonal_assessment):
      prev, years, years_std = previous(seq, n, next = True)
      prev[0] = -1
      V1_sigma = [prev * years_std[i] for i in range(years)]
      f1 = seq - np.hstack(V1_sigma)[:-n]
      if next:
          return f1
      else:
          return f1

    def second_trend_assessment(seq, n, next = False, previous = first_trend_assessment):
      f1 = previous(seq, n, next = True)
      point_0 = (5 * f1.iloc[0] + 2 * f1.iloc[1] - f1.iloc[2])/6
      point_n = (5 * f1.iloc[-1] + 2 * f1.iloc[-2] - f1.iloc[-3])/6
      point_1 = f1.rolling(3, center=True).mean()[2]
      point_n1 = f1.rolling(3, center=True).mean()[len(f1) - 1]
      f2 = f1.rolling(window=5, center=True).mean()
      f2[0:2] = (point_0, point_1)
      f2[-2:] = (point_n1, point_n)
      if next:
          return f1
      else:
          return f2

    def second_seasonal_assessment(seq, n, next = False, previous = second_trend_assessment):
      def split_sequence(sequence, period):
          it = iter(sequence)
          while True:
              chunk = tuple(islice(it, period))
              if not chunk:
                  return
              yield np.array(chunk)

      f2 = previous(seq, n, next = True)
      l2 = seq - f2
      subsequences2 = list(split_sequence(l2, n))
      years_std2 = []

      for i in subsequences2:
          years_std2.append(i.std(ddof=1))
      years2 = subsequences2

      x = np.array(years2, dtype=object)[:-2]
      y = np.array(years_std2)[:-2]
      l_tilda_years2 = [x / y for x,y in zip(x, y)]
      padded_arrays2 = [np.pad(arr, (0, n - len(arr)), 'constant') for arr in l_tilda_years2]
      V2 = np.vstack(padded_arrays2).mean(axis=0)
      if next:
          return V2, l2, years2, years_std2
      else:
          return V2


    def residuals(seq, n, previous = second_seasonal_assessment):
      V2, l2, years2, years_std2 = previous(seq, n, next = True)
      V2_sigma = [V2 * years_std2[i] for i in range(len(years2))]

      err = l2[:-1] - np.hstack(V2_sigma)[:-1]
      return err

    items = [preliminary_trend_assessment,
             first_trend_assessment,
             second_trend_assessment,
             first_seasonal_assessment,
             second_seasonal_assessment,
             residuals]
    titles = ['Предварительная оценка тренда',
              'Первая оценка тренда',
              'Вторая оценка тренда',
              'Первая оценка сезонности',
              'Вторая оценка сезонности',
              'Остаточная компонента'
    ]

    fig, axs = plt.subplots(6, 1, figsize=(14, 22))

    for i, ax in enumerate(axs):
        ax.plot(items[i](seq, n))
        ax.set_title(titles[i])
    plt.tight_layout()
    plt.show()
    return None